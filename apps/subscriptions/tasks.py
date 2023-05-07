from celery import shared_task
from stripe.error import StripeError

from .helpers import sync_subscription_model_with_stripe
from apps.teams.models import Team


@shared_task
def sync_subscriptions_task():
    for team in Team.get_items_needing_sync():
        try:
            sync_subscription_model_with_stripe(team)
        except StripeError as e:
            raise  # you may want to swallow and log this error so it doesn't prevent other subscriptions from syncing
