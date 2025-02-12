import stripe
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from djstripe.models import Subscription
from djstripe.utils import CURRENCY_SIGILS
from djstripe.settings import djstripe_settings

from stripe.api_resources.billing_portal.session import Session as BillingPortalSession
from stripe.api_resources.checkout import Session as CheckoutSession

from .exceptions import SubscriptionConfigError
from apps.teams.models import Team
from apps.users.models import CustomUser
from apps.web.meta import absolute_url


def get_friendly_currency_amount(plan):
    # modified from djstripe's version to only include sigil or currency, but not both
    if plan.amount is None:
        return 'Unknown'
    return get_price_display_with_currency(plan.amount, plan.currency)


def get_price_display_with_currency(amount: float, currency: str) -> str:
    currency = currency.upper()
    sigil = CURRENCY_SIGILS.get(currency, "")
    if sigil:
        return "{sigil}{amount:.2f}".format(sigil=sigil, amount=amount)
    else:
        return "{amount:.2f} {currency}".format(amount=amount, currency=currency)


def get_subscription_urls(subscription_holder):
    # get URLs for subscription helpers
    url_bases = [
        'subscription_details',
        'create_stripe_portal_session',
        'subscription_demo',
        'subscription_gated_page',
        # checkout urls
        'create_checkout_session',
        'checkout_success',
        'checkout_canceled',
    ]

    def _construct_url(base):
        return reverse(f'subscriptions_team:{base}', args=[subscription_holder.slug])

    return {
        url_base: _construct_url(url_base) for url_base in url_bases
    }


def get_payment_metadata_from_request(request):
    return {
        'user_id': request.user.id,
        'user_email': request.user.email,
        'team_id': request.team.id,
    }


def get_stripe_module():
    """Gets the Stripe API module, with the API key properly populated"""
    stripe.api_key = djstripe_settings.STRIPE_SECRET_KEY
    return stripe


def create_stripe_checkout_session(subscription_holder: Team, stripe_price_id: str, user: CustomUser) -> CheckoutSession:
    stripe = get_stripe_module()

    subscription_urls = get_subscription_urls(subscription_holder)
    success_url = absolute_url(reverse('subscriptions_team:checkout_success', args=[subscription_holder.slug]))
    cancel_url = absolute_url(reverse('subscriptions_team:checkout_canceled', args=[subscription_holder.slug]))

    customer_kwargs = {}
    if user.customer:
        customer_kwargs['customer'] = user.customer.id
    else:
        customer_kwargs['customer_email'] = user.email

    checkout_session = stripe.checkout.Session.create(
        success_url=success_url + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=cancel_url,
        payment_method_types=['card'],
        mode='subscription',
        client_reference_id=subscription_holder.id,
        line_items=[{
            'price': stripe_price_id,
            # For metered billing, do not pass quantity
            'quantity': subscription_holder.get_quantity(),
        }],
        allow_promotion_codes=True,
        subscription_data={
            'description': str(subscription_holder),
        },
        **customer_kwargs,
    )
    return checkout_session


def create_stripe_portal_session(subscription_holder: Team) -> BillingPortalSession:
    stripe = get_stripe_module()
    if not subscription_holder.subscription or not subscription_holder.subscription.customer:
        raise SubscriptionConfigError(_("Whoops, we couldn't find a subscription associated with your account!"))

    subscription_urls = get_subscription_urls(subscription_holder)
    portal_session = stripe.billing_portal.Session.create(
        customer=subscription_holder.subscription.customer.id,
        return_url=absolute_url(subscription_urls['subscription_details']),
    )
    return portal_session


def provision_subscription(subscription_holder: Team, subscription_id: str) -> Subscription:
    stripe = get_stripe_module()
    subscription = stripe.Subscription.retrieve(subscription_id)
    djstripe_subscription = Subscription.sync_from_stripe_data(subscription)
    subscription_holder.subscription = djstripe_subscription
    subscription_holder.save()
    return djstripe_subscription


def sync_subscription_model_with_stripe(subscription_model: Team):
    """
    Syncs a model that uses a subscription with Stripe - updating the quantity associated with
    the subscription, if necessary.
    """
    # snapshot the time before the sync happens, in case the model changes while it is being synced
    sync_time = timezone.now()
    stripe = get_stripe_module()
    # retrieve and update the quantity on the subscription
    # modified from https://stripe.com/docs/billing/subscriptions/per-seat#change-price
    current_subscription = stripe.Subscription.retrieve(subscription_model.subscription.id)

    old_quantity = current_subscription.quantity
    new_quantity = subscription_model.get_quantity()

    if old_quantity != new_quantity:
        stripe.Subscription.modify(
            subscription_model.subscription.id,
            items=[{
                'id': current_subscription['items']['data'][0].id,
                'quantity': subscription_model.get_quantity(),
            }],
        )
    subscription_model.last_synced_with_stripe = sync_time
    subscription_model.save()
