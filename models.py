# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CloudflareCloudflaredns(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    domain = models.CharField(unique=True, max_length=200, blank=True, null=True)
    olddns = models.TextField(db_column='oldDNS', blank=True, null=True)  # Field name made lowercase.
    newdns = models.TextField(db_column='newDNS', blank=True, null=True)  # Field name made lowercase.
    getdns = models.BooleanField(db_column='getDNS')  # Field name made lowercase.
    updatedns = models.BooleanField(db_column='updateDNS')  # Field name made lowercase.
    resp = models.TextField(db_column='resP', blank=True, null=True)  # Field name made lowercase.
    cloudflaremodel = models.ForeignKey('CloudflareCloudflaremodel', models.DO_NOTHING)
    deletedns = models.TextField(db_column='deleteDNS', blank=True, null=True)  # Field name made lowercase.
    cloudid = models.CharField(unique=True, max_length=200, blank=True, null=True)
    cloudname = models.CharField(unique=True, max_length=200, blank=True, null=True)
    pagerule = models.BooleanField(db_column='pageRule')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cloudflare_cloudflaredns'


class CloudflareCloudflaremodel(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    email = models.CharField(max_length=254, blank=True, null=True)
    key = models.CharField(max_length=60, blank=True, null=True)
    nameservers = models.TextField(db_column='nameServers', blank=True, null=True)  # Field name made lowercase.
    resp = models.TextField(db_column='resP', blank=True, null=True)  # Field name made lowercase.
    user = models.ForeignKey('UsersCustomuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Cloudflare_cloudflaremodel'


class ContentKeywordideas(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    keywords = models.CharField(max_length=300, blank=True, null=True)
    pageurl = models.CharField(db_column='pageUrl', max_length=500, blank=True, null=True)  # Field name made lowercase.
    result = models.TextField(blank=True, null=True)
    user = models.ForeignKey('UsersCustomuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Content_keywordideas'


class ContentSpintax7(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    runspintax = models.BooleanField(db_column='runSpintax')  # Field name made lowercase.
    topic = models.CharField(max_length=300, blank=True, null=True)
    content1 = models.TextField(blank=True, null=True)
    content2 = models.TextField(blank=True, null=True)
    content3 = models.TextField(blank=True, null=True)
    content4 = models.TextField(blank=True, null=True)
    content5 = models.TextField(blank=True, null=True)
    content6 = models.TextField(blank=True, null=True)
    content7 = models.TextField(blank=True, null=True)
    user = models.ForeignKey('UsersCustomuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Content_spintax7'


class ContentYacss(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    runapp = models.BooleanField(db_column='runApp')  # Field name made lowercase.
    topic = models.CharField(max_length=300, blank=True, null=True)
    questions = models.TextField(blank=True, null=True)
    answers = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    user = models.ForeignKey('UsersCustomuser', models.DO_NOTHING)
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Content_yacss'


class SitenetworkBacklinks(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    backlink = models.CharField(max_length=200, blank=True, null=True)
    anchor = models.CharField(max_length=60, blank=True, null=True)
    rebuildpage = models.CharField(db_column='rebuildPage', max_length=60, blank=True, null=True)  # Field name made lowercase.
    numberoflinks = models.IntegerField(db_column='numberOfLinks', blank=True, null=True)  # Field name made lowercase.
    dr = models.IntegerField(db_column='DR', blank=True, null=True)  # Field name made lowercase.
    traffic = models.IntegerField(blank=True, null=True)
    page = models.ForeignKey('SitenetworkSites', models.DO_NOTHING, db_column='Page_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SiteNetwork_backlinks'


class SitenetworkDigitalproperty(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    domain = models.CharField(unique=True, max_length=200, blank=True, null=True)
    nameserver = models.TextField(blank=True, null=True)
    registrar = models.CharField(max_length=300, blank=True, null=True)
    expiredate = models.DateField(db_column='expireDate', blank=True, null=True)  # Field name made lowercase.
    traffic = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=300, blank=True, null=True)
    niche = models.CharField(max_length=300, blank=True, null=True)
    importance = models.CharField(max_length=300, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    user = models.ForeignKey('UsersCustomuser', models.DO_NOTHING)
    whois = models.BooleanField(db_column='Whois')  # Field name made lowercase.
    backlinks = models.TextField(blank=True, null=True)
    urlshortner = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SiteNetwork_digitalproperty'


class SitenetworkSites(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    site = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=60, blank=True, null=True)
    niche = models.CharField(max_length=60, blank=True, null=True)
    user = models.ForeignKey('UsersCustomuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'SiteNetwork_sites'


class AccountEmailaddress(models.Model):
    email = models.CharField(unique=True, max_length=254)
    verified = models.BooleanField()
    primary = models.BooleanField()
    user = models.ForeignKey('UsersCustomuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_emailaddress'


class AccountEmailconfirmation(models.Model):
    created = models.DateTimeField()
    sent = models.DateTimeField(blank=True, null=True)
    key = models.CharField(unique=True, max_length=64)
    email_address = models.ForeignKey(AccountEmailaddress, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_emailconfirmation'


class ApiUserapikey(models.Model):
    id = models.CharField(primary_key=True, max_length=150)
    prefix = models.CharField(unique=True, max_length=8)
    hashed_key = models.CharField(max_length=150)
    created = models.DateTimeField()
    name = models.CharField(max_length=50)
    revoked = models.BooleanField()
    expiry_date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey('UsersCustomuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_userapikey'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class ContentBlogindexpage(models.Model):
    page_ptr = models.OneToOneField('WagtailcorePage', models.DO_NOTHING, primary_key=True)
    intro = models.TextField()

    class Meta:
        managed = False
        db_table = 'content_blogindexpage'


class ContentBlogpage(models.Model):
    page_ptr = models.OneToOneField('WagtailcorePage', models.DO_NOTHING, primary_key=True)
    date = models.DateField()
    intro = models.CharField(max_length=250)
    body = models.TextField()

    class Meta:
        managed = False
        db_table = 'content_blogpage'


class ContentBlogpagegalleryimage(models.Model):
    sort_order = models.IntegerField(blank=True, null=True)
    caption = models.CharField(max_length=250)
    image = models.ForeignKey('WagtailimagesImage', models.DO_NOTHING)
    page = models.ForeignKey(ContentBlogpage, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'content_blogpagegalleryimage'


class ContentContentpage(models.Model):
    page_ptr = models.OneToOneField('WagtailcorePage', models.DO_NOTHING, primary_key=True)
    body = models.TextField()

    class Meta:
        managed = False
        db_table = 'content_contentpage'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('UsersCustomuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoCronCronjoblock(models.Model):
    job_name = models.CharField(unique=True, max_length=200)
    locked = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'django_cron_cronjoblock'


class DjangoCronCronjoblog(models.Model):
    code = models.CharField(max_length=64)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_success = models.BooleanField()
    message = models.TextField()
    ran_at_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_cron_cronjoblog'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjangoSite(models.Model):
    domain = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'django_site'


class DjstripeAccount(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    business_profile = models.JSONField(blank=True, null=True)
    business_type = models.CharField(max_length=10)
    charges_enabled = models.BooleanField()
    country = models.CharField(max_length=2)
    company = models.JSONField(blank=True, null=True)
    default_currency = models.CharField(max_length=3)
    details_submitted = models.BooleanField()
    email = models.CharField(max_length=255)
    individual = models.JSONField(blank=True, null=True)
    payouts_enabled = models.BooleanField(blank=True, null=True)
    product_description = models.CharField(max_length=255)
    requirements = models.JSONField(blank=True, null=True)
    settings = models.JSONField(blank=True, null=True)
    type = models.CharField(max_length=8)
    tos_acceptance = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_account'


class DjstripeApikey(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    livemode = models.BooleanField()
    created = models.DateTimeField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    id = models.CharField(max_length=255)
    type = models.CharField(max_length=11)
    name = models.CharField(max_length=100)
    secret = models.CharField(unique=True, max_length=128)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_apikey'


class DjstripeApplicationfee(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    amount = models.BigIntegerField()
    amount_refunded = models.BigIntegerField()
    currency = models.CharField(max_length=3)
    refunded = models.BooleanField()
    balance_transaction = models.ForeignKey('DjstripeBalancetransaction', models.DO_NOTHING)
    charge = models.ForeignKey('DjstripeCharge', models.DO_NOTHING)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)
    account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'djstripe_applicationfee'


class DjstripeApplicationfeerefund(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    amount = models.BigIntegerField()
    currency = models.CharField(max_length=3)
    balance_transaction = models.ForeignKey('DjstripeBalancetransaction', models.DO_NOTHING)
    fee = models.ForeignKey(DjstripeApplicationfee, models.DO_NOTHING)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_applicationfeerefund'


class DjstripeBalancetransaction(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    amount = models.BigIntegerField()
    available_on = models.DateTimeField()
    currency = models.CharField(max_length=3)
    exchange_rate = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True)
    fee = models.BigIntegerField()
    fee_details = models.JSONField()
    net = models.BigIntegerField()
    status = models.CharField(max_length=9)
    type = models.CharField(max_length=29)
    reporting_category = models.CharField(max_length=29)
    source = models.CharField(max_length=255)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_balancetransaction'


class DjstripeBankaccount(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    account_holder_name = models.TextField()
    account_holder_type = models.CharField(max_length=10)
    bank_name = models.CharField(max_length=255)
    country = models.CharField(max_length=2)
    currency = models.CharField(max_length=3)
    default_for_currency = models.BooleanField(blank=True, null=True)
    fingerprint = models.CharField(max_length=16)
    last4 = models.CharField(max_length=4)
    routing_number = models.CharField(max_length=255)
    status = models.CharField(max_length=19)
    account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)
    customer = models.ForeignKey('DjstripeCustomer', models.DO_NOTHING, blank=True, null=True)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_bankaccount'


class DjstripeCard(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    address_city = models.TextField()
    address_country = models.TextField()
    address_line1 = models.TextField()
    address_line1_check = models.CharField(max_length=11)
    address_line2 = models.TextField()
    address_state = models.TextField()
    address_zip = models.TextField()
    address_zip_check = models.CharField(max_length=11)
    brand = models.CharField(max_length=16)
    country = models.CharField(max_length=2)
    cvc_check = models.CharField(max_length=11)
    dynamic_last4 = models.CharField(max_length=4)
    exp_month = models.IntegerField()
    exp_year = models.IntegerField()
    fingerprint = models.CharField(max_length=16)
    funding = models.CharField(max_length=7)
    last4 = models.CharField(max_length=4)
    name = models.TextField()
    tokenization_method = models.CharField(max_length=11)
    customer = models.ForeignKey('DjstripeCustomer', models.DO_NOTHING, blank=True, null=True)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)
    account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)
    default_for_currency = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_card'


class DjstripeCharge(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    amount_refunded = models.DecimalField(max_digits=11, decimal_places=2)
    captured = models.BooleanField()
    currency = models.CharField(max_length=3)
    failure_code = models.CharField(max_length=42)
    failure_message = models.TextField()
    fraud_details = models.JSONField(blank=True, null=True)
    outcome = models.JSONField(blank=True, null=True)
    paid = models.BooleanField()
    payment_method_details = models.JSONField(blank=True, null=True)
    receipt_email = models.TextField()
    receipt_number = models.CharField(max_length=14)
    receipt_url = models.TextField()
    refunded = models.BooleanField()
    shipping = models.JSONField(blank=True, null=True)
    statement_descriptor = models.CharField(max_length=22, blank=True, null=True)
    status = models.CharField(max_length=9)
    transfer_group = models.CharField(max_length=255, blank=True, null=True)
    on_behalf_of = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)
    customer = models.ForeignKey('DjstripeCustomer', models.DO_NOTHING, blank=True, null=True)
    dispute = models.ForeignKey('DjstripeDispute', models.DO_NOTHING, blank=True, null=True)
    invoice = models.ForeignKey('DjstripeInvoice', models.DO_NOTHING, blank=True, null=True)
    source = models.ForeignKey('DjstripeDjstripepaymentmethod', models.DO_NOTHING, blank=True, null=True)
    transfer = models.ForeignKey('DjstripeTransfer', models.DO_NOTHING, blank=True, null=True)
    balance_transaction = models.ForeignKey(DjstripeBalancetransaction, models.DO_NOTHING, blank=True, null=True)
    payment_intent = models.ForeignKey('DjstripePaymentintent', models.DO_NOTHING, blank=True, null=True)
    payment_method = models.ForeignKey('DjstripePaymentmethod', models.DO_NOTHING, blank=True, null=True)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)
    amount_captured = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    application = models.CharField(max_length=255)
    application_fee_amount = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    billing_details = models.JSONField(blank=True, null=True)
    calculated_statement_descriptor = models.CharField(max_length=22)
    disputed = models.BooleanField()
    source_transfer = models.ForeignKey('DjstripeTransfer', models.DO_NOTHING, blank=True, null=True)
    statement_descriptor_suffix = models.CharField(max_length=22, blank=True, null=True)
    transfer_data = models.JSONField(blank=True, null=True)
    application_fee = models.ForeignKey(DjstripeApplicationfee, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_charge'


class DjstripeCountryspec(models.Model):
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    id = models.CharField(primary_key=True, max_length=2)
    default_currency = models.CharField(max_length=3)
    supported_bank_account_currencies = models.JSONField()
    supported_payment_currencies = models.JSONField()
    supported_payment_methods = models.JSONField()
    supported_transfer_countries = models.JSONField()
    verification_fields = models.JSONField()

    class Meta:
        managed = False
        db_table = 'djstripe_countryspec'


class DjstripeCoupon(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    id = models.CharField(max_length=500)
    amount_off = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=3, blank=True, null=True)
    duration = models.CharField(max_length=9)
    duration_in_months = models.IntegerField(blank=True, null=True)
    max_redemptions = models.IntegerField(blank=True, null=True)
    percent_off = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    redeem_by = models.DateTimeField(blank=True, null=True)
    times_redeemed = models.IntegerField()
    name = models.TextField()
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_coupon'
        unique_together = (('id', 'livemode'),)


class DjstripeCustomer(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    balance = models.BigIntegerField(blank=True, null=True)
    currency = models.CharField(max_length=3)
    delinquent = models.BooleanField(blank=True, null=True)
    coupon_start = models.DateTimeField(blank=True, null=True)
    coupon_end = models.DateTimeField(blank=True, null=True)
    email = models.TextField()
    shipping = models.JSONField(blank=True, null=True)
    date_purged = models.DateTimeField(blank=True, null=True)
    coupon = models.ForeignKey(DjstripeCoupon, models.DO_NOTHING, blank=True, null=True)
    default_source = models.ForeignKey('DjstripeDjstripepaymentmethod', models.DO_NOTHING, blank=True, null=True)
    subscriber = models.ForeignKey('UsersCustomuser', models.DO_NOTHING, blank=True, null=True)
    address = models.JSONField(blank=True, null=True)
    invoice_prefix = models.CharField(max_length=255)
    invoice_settings = models.JSONField(blank=True, null=True)
    name = models.TextField()
    phone = models.TextField()
    preferred_locales = models.JSONField(blank=True, null=True)
    tax_exempt = models.CharField(max_length=7)
    default_payment_method = models.ForeignKey('DjstripePaymentmethod', models.DO_NOTHING, blank=True, null=True)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)
    deleted = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_customer'
        unique_together = (('subscriber', 'livemode', 'djstripe_owner_account'),)


class DjstripeDispute(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    amount = models.BigIntegerField()
    currency = models.CharField(max_length=3)
    evidence = models.JSONField()
    evidence_details = models.JSONField()
    is_charge_refundable = models.BooleanField()
    reason = models.CharField(max_length=25)
    status = models.CharField(max_length=22)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)
    balance_transaction = models.ForeignKey(DjstripeBalancetransaction, models.DO_NOTHING, blank=True, null=True)
    charge = models.ForeignKey(DjstripeCharge, models.DO_NOTHING, blank=True, null=True)
    payment_intent = models.ForeignKey('DjstripePaymentintent', models.DO_NOTHING, blank=True, null=True)
    balance_transactions = models.JSONField()

    class Meta:
        managed = False
        db_table = 'djstripe_dispute'


class DjstripeDjstripeinvoicedefaulttaxrate(models.Model):
    invoice = models.ForeignKey('DjstripeInvoice', models.DO_NOTHING)
    taxrate = models.ForeignKey('DjstripeTaxrate', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'djstripe_djstripeinvoicedefaulttaxrate'
        unique_together = (('invoice', 'taxrate'),)


class DjstripeDjstripeinvoiceitemtaxrate(models.Model):
    invoiceitem = models.ForeignKey('DjstripeInvoiceitem', models.DO_NOTHING)
    taxrate = models.ForeignKey('DjstripeTaxrate', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'djstripe_djstripeinvoiceitemtaxrate'
        unique_together = (('invoiceitem', 'taxrate'),)


class DjstripeDjstripeinvoicetotaltaxamount(models.Model):
    amount = models.BigIntegerField()
    inclusive = models.BooleanField()
    invoice = models.ForeignKey('DjstripeInvoice', models.DO_NOTHING)
    tax_rate = models.ForeignKey('DjstripeTaxrate', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'djstripe_djstripeinvoicetotaltaxamount'
        unique_together = (('invoice', 'tax_rate'),)


class DjstripeDjstripepaymentmethod(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    type = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'djstripe_djstripepaymentmethod'


class DjstripeDjstripesubscriptiondefaulttaxrate(models.Model):
    subscription = models.ForeignKey('DjstripeSubscription', models.DO_NOTHING)
    taxrate = models.ForeignKey('DjstripeTaxrate', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'djstripe_djstripesubscriptiondefaulttaxrate'
        unique_together = (('subscription', 'taxrate'),)


class DjstripeDjstripesubscriptionitemtaxrate(models.Model):
    subscriptionitem = models.ForeignKey('DjstripeSubscriptionitem', models.DO_NOTHING)
    taxrate = models.ForeignKey('DjstripeTaxrate', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'djstripe_djstripesubscriptionitemtaxrate'
        unique_together = (('subscriptionitem', 'taxrate'),)


class DjstripeDjstripeupcominginvoicetotaltaxamount(models.Model):
    amount = models.BigIntegerField()
    inclusive = models.BooleanField()
    invoice = models.ForeignKey('DjstripeUpcominginvoice', models.DO_NOTHING)
    tax_rate = models.ForeignKey('DjstripeTaxrate', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'djstripe_djstripeupcominginvoicetotaltaxamount'
        unique_together = (('invoice', 'tax_rate'),)


class DjstripeEvent(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    api_version = models.CharField(max_length=15)
    data = models.JSONField()
    request_id = models.CharField(max_length=50)
    idempotency_key = models.TextField()
    type = models.CharField(max_length=250)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_event'


class DjstripeFile(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    filename = models.CharField(max_length=255)
    purpose = models.CharField(max_length=35)
    size = models.IntegerField()
    type = models.CharField(max_length=4)
    url = models.CharField(max_length=200)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_file'


class DjstripeFilelink(models.Model):
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    url = models.CharField(max_length=200)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)
    file = models.ForeignKey(DjstripeFile, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'djstripe_filelink'


class DjstripeIdempotencykey(models.Model):
    uuid = models.UUIDField(primary_key=True)
    action = models.CharField(max_length=100)
    livemode = models.BooleanField()
    created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'djstripe_idempotencykey'
        unique_together = (('action', 'livemode'),)


class DjstripeInvoice(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    amount_due = models.DecimalField(max_digits=11, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    amount_remaining = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    application_fee_amount = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    attempt_count = models.IntegerField()
    attempted = models.BooleanField()
    collection_method = models.CharField(max_length=20, blank=True, null=True)
    currency = models.CharField(max_length=3)
    due_date = models.DateTimeField(blank=True, null=True)
    ending_balance = models.BigIntegerField(blank=True, null=True)
    hosted_invoice_url = models.TextField()
    invoice_pdf = models.TextField()
    next_payment_attempt = models.DateTimeField(blank=True, null=True)
    number = models.CharField(max_length=64)
    paid = models.BooleanField()
    period_end = models.DateTimeField()
    period_start = models.DateTimeField()
    receipt_number = models.CharField(max_length=64, blank=True, null=True)
    starting_balance = models.BigIntegerField()
    statement_descriptor = models.CharField(max_length=22)
    subscription_proration_date = models.DateTimeField(blank=True, null=True)
    subtotal = models.DecimalField(max_digits=11, decimal_places=2)
    tax = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=11, decimal_places=2)
    webhooks_delivered_at = models.DateTimeField(blank=True, null=True)
    charge = models.OneToOneField(DjstripeCharge, models.DO_NOTHING, blank=True, null=True)
    customer = models.ForeignKey(DjstripeCustomer, models.DO_NOTHING)
    subscription = models.ForeignKey('DjstripeSubscription', models.DO_NOTHING, blank=True, null=True)
    auto_advance = models.BooleanField(blank=True, null=True)
    status_transitions = models.JSONField(blank=True, null=True)
    payment_intent = models.OneToOneField('DjstripePaymentintent', models.DO_NOTHING, blank=True, null=True)
    account_country = models.CharField(max_length=2)
    account_name = models.TextField()
    billing_reason = models.CharField(max_length=22)
    customer_address = models.JSONField(blank=True, null=True)
    customer_email = models.TextField()
    customer_name = models.TextField()
    customer_phone = models.TextField()
    customer_shipping = models.JSONField(blank=True, null=True)
    customer_tax_exempt = models.CharField(max_length=7)
    default_payment_method = models.ForeignKey('DjstripePaymentmethod', models.DO_NOTHING, blank=True, null=True)
    footer = models.TextField()
    post_payment_credit_notes_amount = models.BigIntegerField(blank=True, null=True)
    pre_payment_credit_notes_amount = models.BigIntegerField(blank=True, null=True)
    threshold_reason = models.JSONField(blank=True, null=True)
    status = models.CharField(max_length=13)
    discount = models.JSONField(blank=True, null=True)
    default_source = models.ForeignKey(DjstripeDjstripepaymentmethod, models.DO_NOTHING, blank=True, null=True)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_invoice'


class DjstripeInvoiceitem(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    currency = models.CharField(max_length=3)
    date = models.DateTimeField()
    discountable = models.BooleanField()
    period = models.JSONField()
    period_end = models.DateTimeField()
    period_start = models.DateTimeField()
    proration = models.BooleanField()
    quantity = models.IntegerField(blank=True, null=True)
    customer = models.ForeignKey(DjstripeCustomer, models.DO_NOTHING)
    invoice = models.ForeignKey(DjstripeInvoice, models.DO_NOTHING, blank=True, null=True)
    plan = models.ForeignKey('DjstripePlan', models.DO_NOTHING, blank=True, null=True)
    subscription = models.ForeignKey('DjstripeSubscription', models.DO_NOTHING, blank=True, null=True)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)
    unit_amount = models.BigIntegerField(blank=True, null=True)
    unit_amount_decimal = models.DecimalField(max_digits=19, decimal_places=12, blank=True, null=True)
    price = models.ForeignKey('DjstripePrice', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_invoiceitem'


class DjstripeMandate(models.Model):
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    customer_acceptance = models.JSONField()
    payment_method_details = models.JSONField()
    status = models.CharField(max_length=8)
    type = models.CharField(max_length=10)
    multi_use = models.JSONField(blank=True, null=True)
    single_use = models.JSONField(blank=True, null=True)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)
    payment_method = models.ForeignKey('DjstripePaymentmethod', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'djstripe_mandate'


class DjstripePaymentintent(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    amount = models.BigIntegerField()
    amount_capturable = models.BigIntegerField()
    amount_received = models.BigIntegerField()
    canceled_at = models.DateTimeField(blank=True, null=True)
    cancellation_reason = models.CharField(max_length=21)
    capture_method = models.CharField(max_length=9)
    client_secret = models.TextField()
    confirmation_method = models.CharField(max_length=9)
    currency = models.CharField(max_length=3)
    description = models.TextField()
    last_payment_error = models.JSONField(blank=True, null=True)
    next_action = models.JSONField(blank=True, null=True)
    payment_method_types = models.JSONField()
    receipt_email = models.CharField(max_length=255)
    setup_future_usage = models.CharField(max_length=11, blank=True, null=True)
    shipping = models.JSONField(blank=True, null=True)
    statement_descriptor = models.CharField(max_length=22)
    status = models.CharField(max_length=23)
    transfer_data = models.JSONField(blank=True, null=True)
    transfer_group = models.CharField(max_length=255)
    customer = models.ForeignKey(DjstripeCustomer, models.DO_NOTHING, blank=True, null=True)
    on_behalf_of = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)
    payment_method = models.ForeignKey('DjstripePaymentmethod', models.DO_NOTHING, blank=True, null=True)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_paymentintent'


class DjstripePaymentmethod(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    billing_details = models.JSONField()
    card = models.JSONField(blank=True, null=True)
    card_present = models.JSONField(blank=True, null=True)
    type = models.CharField(max_length=17)
    customer = models.ForeignKey(DjstripeCustomer, models.DO_NOTHING, blank=True, null=True)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)
    alipay = models.JSONField(blank=True, null=True)
    au_becs_debit = models.JSONField(blank=True, null=True)
    bacs_debit = models.JSONField(blank=True, null=True)
    bancontact = models.JSONField(blank=True, null=True)
    eps = models.JSONField(blank=True, null=True)
    fpx = models.JSONField(blank=True, null=True)
    giropay = models.JSONField(blank=True, null=True)
    ideal = models.JSONField(blank=True, null=True)
    interac_present = models.JSONField(blank=True, null=True)
    oxxo = models.JSONField(blank=True, null=True)
    p24 = models.JSONField(blank=True, null=True)
    sepa_debit = models.JSONField(blank=True, null=True)
    sofort = models.JSONField(blank=True, null=True)
    acss_debit = models.JSONField(blank=True, null=True)
    afterpay_clearpay = models.JSONField(blank=True, null=True)
    boleto = models.JSONField(blank=True, null=True)
    grabpay = models.JSONField(blank=True, null=True)
    wechat_pay = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_paymentmethod'


class DjstripePayout(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    arrival_date = models.DateTimeField()
    currency = models.CharField(max_length=3)
    failure_code = models.CharField(max_length=23)
    failure_message = models.TextField()
    method = models.CharField(max_length=8)
    statement_descriptor = models.CharField(max_length=255)
    status = models.CharField(max_length=10)
    type = models.CharField(max_length=12)
    destination = models.ForeignKey(DjstripeBankaccount, models.DO_NOTHING, blank=True, null=True)
    balance_transaction = models.ForeignKey(DjstripeBalancetransaction, models.DO_NOTHING, blank=True, null=True)
    failure_balance_transaction = models.ForeignKey(DjstripeBalancetransaction, models.DO_NOTHING, blank=True, null=True)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)
    automatic = models.BooleanField()
    source_type = models.CharField(max_length=12)

    class Meta:
        managed = False
        db_table = 'djstripe_payout'


class DjstripePlan(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    active = models.BooleanField()
    aggregate_usage = models.CharField(max_length=18)
    amount = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    billing_scheme = models.CharField(max_length=8)
    currency = models.CharField(max_length=3)
    interval = models.CharField(max_length=5)
    interval_count = models.IntegerField(blank=True, null=True)
    nickname = models.TextField()
    tiers = models.JSONField(blank=True, null=True)
    tiers_mode = models.CharField(max_length=9, blank=True, null=True)
    transform_usage = models.JSONField(blank=True, null=True)
    trial_period_days = models.IntegerField(blank=True, null=True)
    usage_type = models.CharField(max_length=8)
    product = models.ForeignKey('DjstripeProduct', models.DO_NOTHING, blank=True, null=True)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)
    amount_decimal = models.DecimalField(max_digits=19, decimal_places=12, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_plan'


class DjstripePrice(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    active = models.BooleanField()
    currency = models.CharField(max_length=3)
    nickname = models.CharField(max_length=250)
    recurring = models.JSONField(blank=True, null=True)
    type = models.CharField(max_length=9)
    unit_amount = models.BigIntegerField(blank=True, null=True)
    unit_amount_decimal = models.DecimalField(max_digits=19, decimal_places=12, blank=True, null=True)
    billing_scheme = models.CharField(max_length=8)
    tiers = models.JSONField(blank=True, null=True)
    tiers_mode = models.CharField(max_length=9, blank=True, null=True)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey('DjstripeProduct', models.DO_NOTHING)
    lookup_key = models.CharField(max_length=250, blank=True, null=True)
    transform_quantity = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_price'


class DjstripeProduct(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    name = models.TextField()
    type = models.CharField(max_length=7)
    active = models.BooleanField(blank=True, null=True)
    attributes = models.JSONField(blank=True, null=True)
    caption = models.TextField()
    deactivate_on = models.JSONField(blank=True, null=True)
    images = models.JSONField(blank=True, null=True)
    package_dimensions = models.JSONField(blank=True, null=True)
    shippable = models.BooleanField(blank=True, null=True)
    url = models.CharField(max_length=799, blank=True, null=True)
    statement_descriptor = models.CharField(max_length=22)
    unit_label = models.CharField(max_length=12)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_product'


class DjstripeRefund(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    amount = models.BigIntegerField()
    currency = models.CharField(max_length=3)
    failure_reason = models.CharField(max_length=24)
    reason = models.CharField(max_length=25)
    receipt_number = models.CharField(max_length=9)
    status = models.CharField(max_length=9)
    charge = models.ForeignKey(DjstripeCharge, models.DO_NOTHING)
    balance_transaction = models.ForeignKey(DjstripeBalancetransaction, models.DO_NOTHING, blank=True, null=True)
    failure_balance_transaction = models.ForeignKey(DjstripeBalancetransaction, models.DO_NOTHING, blank=True, null=True)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_refund'


class DjstripeScheduledqueryrun(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    data_load_time = models.DateTimeField()
    error = models.JSONField(blank=True, null=True)
    result_available_until = models.DateTimeField()
    sql = models.TextField()
    status = models.CharField(max_length=9)
    title = models.TextField()
    file = models.ForeignKey(DjstripeFile, models.DO_NOTHING, blank=True, null=True)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_scheduledqueryrun'


class DjstripeSession(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    billing_address_collection = models.CharField(max_length=8)
    cancel_url = models.TextField()
    client_reference_id = models.TextField()
    customer_email = models.CharField(max_length=255)
    display_items = models.JSONField(blank=True, null=True)
    locale = models.CharField(max_length=255)
    payment_method_types = models.JSONField()
    submit_type = models.CharField(max_length=6)
    success_url = models.TextField()
    customer = models.ForeignKey(DjstripeCustomer, models.DO_NOTHING, blank=True, null=True)
    payment_intent = models.ForeignKey(DjstripePaymentintent, models.DO_NOTHING, blank=True, null=True)
    subscription = models.ForeignKey('DjstripeSubscription', models.DO_NOTHING, blank=True, null=True)
    mode = models.CharField(max_length=12)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_session'


class DjstripeSetupintent(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    application = models.CharField(max_length=255)
    cancellation_reason = models.CharField(max_length=21)
    client_secret = models.TextField()
    last_setup_error = models.JSONField(blank=True, null=True)
    next_action = models.JSONField(blank=True, null=True)
    payment_method_types = models.JSONField()
    status = models.CharField(max_length=23)
    usage = models.CharField(max_length=11)
    customer = models.ForeignKey(DjstripeCustomer, models.DO_NOTHING, blank=True, null=True)
    on_behalf_of = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)
    payment_method = models.ForeignKey(DjstripePaymentmethod, models.DO_NOTHING, blank=True, null=True)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_setupintent'


class DjstripeSource(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    amount = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    client_secret = models.CharField(max_length=255)
    currency = models.CharField(max_length=3)
    flow = models.CharField(max_length=17)
    owner = models.JSONField()
    statement_descriptor = models.CharField(max_length=255)
    status = models.CharField(max_length=10)
    type = models.CharField(max_length=20)
    usage = models.CharField(max_length=10)
    code_verification = models.JSONField(blank=True, null=True)
    receiver = models.JSONField(blank=True, null=True)
    redirect = models.JSONField(blank=True, null=True)
    source_data = models.JSONField()
    customer = models.ForeignKey(DjstripeCustomer, models.DO_NOTHING, blank=True, null=True)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_source'


class DjstripeSubscription(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    application_fee_percent = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    collection_method = models.CharField(max_length=20)
    billing_cycle_anchor = models.DateTimeField(blank=True, null=True)
    cancel_at_period_end = models.BooleanField()
    canceled_at = models.DateTimeField(blank=True, null=True)
    current_period_end = models.DateTimeField()
    current_period_start = models.DateTimeField()
    days_until_due = models.IntegerField(blank=True, null=True)
    discount = models.JSONField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    next_pending_invoice_item_invoice = models.DateTimeField(blank=True, null=True)
    pending_invoice_item_interval = models.JSONField(blank=True, null=True)
    pending_update = models.JSONField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=18)
    trial_end = models.DateTimeField(blank=True, null=True)
    trial_start = models.DateTimeField(blank=True, null=True)
    customer = models.ForeignKey(DjstripeCustomer, models.DO_NOTHING)
    plan = models.ForeignKey(DjstripePlan, models.DO_NOTHING, blank=True, null=True)
    pending_setup_intent = models.ForeignKey(DjstripeSetupintent, models.DO_NOTHING, blank=True, null=True)
    default_payment_method = models.ForeignKey(DjstripePaymentmethod, models.DO_NOTHING, blank=True, null=True)
    default_source = models.ForeignKey(DjstripeDjstripepaymentmethod, models.DO_NOTHING, blank=True, null=True)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)
    cancel_at = models.DateTimeField(blank=True, null=True)
    schedule = models.ForeignKey('DjstripeSubscriptionschedule', models.DO_NOTHING, blank=True, null=True)
    billing_thresholds = models.JSONField(blank=True, null=True)
    latest_invoice = models.ForeignKey(DjstripeInvoice, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_subscription'


class DjstripeSubscriptionitem(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    quantity = models.IntegerField(blank=True, null=True)
    plan = models.ForeignKey(DjstripePlan, models.DO_NOTHING)
    subscription = models.ForeignKey(DjstripeSubscription, models.DO_NOTHING)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)
    price = models.ForeignKey(DjstripePrice, models.DO_NOTHING, blank=True, null=True)
    billing_thresholds = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_subscriptionitem'


class DjstripeSubscriptionschedule(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    canceled_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    current_phase = models.JSONField(blank=True, null=True)
    default_settings = models.JSONField(blank=True, null=True)
    end_behavior = models.CharField(max_length=7)
    phases = models.JSONField(blank=True, null=True)
    released_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=11)
    customer = models.ForeignKey(DjstripeCustomer, models.DO_NOTHING)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)
    released_subscription = models.ForeignKey(DjstripeSubscription, models.DO_NOTHING, blank=True, null=True)
    billing_thresholds = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_subscriptionschedule'


class DjstripeTaxid(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    country = models.CharField(max_length=2)
    type = models.CharField(max_length=7)
    value = models.CharField(max_length=50)
    verification = models.JSONField()
    customer = models.ForeignKey(DjstripeCustomer, models.DO_NOTHING)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_taxid'


class DjstripeTaxrate(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    active = models.BooleanField()
    display_name = models.CharField(max_length=50)
    inclusive = models.BooleanField()
    jurisdiction = models.CharField(max_length=50)
    percentage = models.DecimalField(max_digits=7, decimal_places=4)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_taxrate'


class DjstripeTransfer(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    amount_reversed = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=3)
    destination = models.CharField(max_length=255, blank=True, null=True)
    destination_payment = models.CharField(max_length=255, blank=True, null=True)
    reversed = models.BooleanField()
    source_transaction = models.CharField(max_length=255, blank=True, null=True)
    source_type = models.CharField(max_length=16)
    transfer_group = models.CharField(max_length=255)
    balance_transaction = models.ForeignKey(DjstripeBalancetransaction, models.DO_NOTHING, blank=True, null=True)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_transfer'


class DjstripeTransferreversal(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    amount = models.BigIntegerField()
    currency = models.CharField(max_length=3)
    balance_transaction = models.ForeignKey(DjstripeBalancetransaction, models.DO_NOTHING, blank=True, null=True)
    transfer = models.ForeignKey(DjstripeTransfer, models.DO_NOTHING)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_transferreversal'


class DjstripeUpcominginvoice(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    account_country = models.CharField(max_length=2)
    account_name = models.TextField()
    amount_due = models.DecimalField(max_digits=11, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    amount_remaining = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    application_fee_amount = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    attempt_count = models.IntegerField()
    attempted = models.BooleanField()
    auto_advance = models.BooleanField(blank=True, null=True)
    billing_reason = models.CharField(max_length=22)
    collection_method = models.CharField(max_length=20, blank=True, null=True)
    currency = models.CharField(max_length=3)
    customer_address = models.JSONField(blank=True, null=True)
    customer_email = models.TextField()
    customer_name = models.TextField()
    customer_phone = models.TextField()
    customer_shipping = models.JSONField(blank=True, null=True)
    customer_tax_exempt = models.CharField(max_length=7)
    due_date = models.DateTimeField(blank=True, null=True)
    ending_balance = models.BigIntegerField(blank=True, null=True)
    footer = models.TextField()
    hosted_invoice_url = models.TextField()
    invoice_pdf = models.TextField()
    next_payment_attempt = models.DateTimeField(blank=True, null=True)
    number = models.CharField(max_length=64)
    paid = models.BooleanField()
    period_end = models.DateTimeField()
    period_start = models.DateTimeField()
    post_payment_credit_notes_amount = models.BigIntegerField(blank=True, null=True)
    pre_payment_credit_notes_amount = models.BigIntegerField(blank=True, null=True)
    receipt_number = models.CharField(max_length=64, blank=True, null=True)
    starting_balance = models.BigIntegerField()
    statement_descriptor = models.CharField(max_length=22)
    status_transitions = models.JSONField(blank=True, null=True)
    subscription_proration_date = models.DateTimeField(blank=True, null=True)
    subtotal = models.DecimalField(max_digits=11, decimal_places=2)
    tax = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    threshold_reason = models.JSONField(blank=True, null=True)
    total = models.DecimalField(max_digits=11, decimal_places=2)
    webhooks_delivered_at = models.DateTimeField(blank=True, null=True)
    charge = models.OneToOneField(DjstripeCharge, models.DO_NOTHING, blank=True, null=True)
    customer = models.ForeignKey(DjstripeCustomer, models.DO_NOTHING)
    default_payment_method = models.ForeignKey(DjstripePaymentmethod, models.DO_NOTHING, blank=True, null=True)
    payment_intent = models.OneToOneField(DjstripePaymentintent, models.DO_NOTHING, blank=True, null=True)
    subscription = models.ForeignKey(DjstripeSubscription, models.DO_NOTHING, blank=True, null=True)
    status = models.CharField(max_length=13)
    default_source = models.ForeignKey(DjstripeDjstripepaymentmethod, models.DO_NOTHING, blank=True, null=True)
    discount = models.JSONField(blank=True, null=True)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_upcominginvoice'


class DjstripeUsagerecord(models.Model):
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    quantity = models.IntegerField()
    subscription_item = models.ForeignKey(DjstripeSubscriptionitem, models.DO_NOTHING)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)
    action = models.CharField(max_length=9)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_usagerecord'


class DjstripeUsagerecordsummary(models.Model):
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    period = models.JSONField(blank=True, null=True)
    period_end = models.DateTimeField(blank=True, null=True)
    period_start = models.DateTimeField(blank=True, null=True)
    total_usage = models.IntegerField()
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)
    invoice = models.ForeignKey(DjstripeInvoice, models.DO_NOTHING, blank=True, null=True)
    subscription_item = models.ForeignKey(DjstripeSubscriptionitem, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'djstripe_usagerecordsummary'


class DjstripeWebhookendpoint(models.Model):
    djstripe_created = models.DateTimeField()
    djstripe_updated = models.DateTimeField()
    djstripe_id = models.BigAutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=255)
    livemode = models.BooleanField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    api_version = models.CharField(max_length=10)
    enabled_events = models.JSONField()
    secret = models.CharField(max_length=256)
    status = models.CharField(max_length=8)
    url = models.CharField(max_length=2048)
    application = models.CharField(max_length=255)
    djstripe_owner_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)
    djstripe_uuid = models.UUIDField(unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_webhookendpoint'


class DjstripeWebhookeventtrigger(models.Model):
    id = models.BigAutoField(primary_key=True)
    remote_ip = models.GenericIPAddressField()
    headers = models.JSONField()
    body = models.TextField()
    valid = models.BooleanField()
    processed = models.BooleanField()
    exception = models.CharField(max_length=128)
    traceback = models.TextField()
    djstripe_version = models.CharField(max_length=32)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    event = models.ForeignKey(DjstripeEvent, models.DO_NOTHING, blank=True, null=True)
    stripe_trigger_account = models.ForeignKey(DjstripeAccount, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'djstripe_webhookeventtrigger'


class IndexWebsiteDtTracking(models.Model):
    id = models.BigIntegerField(primary_key=True)
    index_web_id = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    updated_by_id = models.IntegerField(blank=True, null=True)
    is_right = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'index_website_dt_tracking'


class IndexerApiUsageTracking(models.Model):
    id = models.IntegerField(primary_key=True)
    api_id = models.IntegerField(blank=True, null=True)
    total = models.CharField(max_length=255, blank=True, null=True)
    date_update = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'indexer_api_usage_tracking'


class IndexerGscverify(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    email = models.CharField(max_length=200)
    htmlfile = models.TextField(db_column='htmlFile')  # Field name made lowercase.
    shortnerwebsite = models.CharField(db_column='shortnerWebsite', max_length=200, blank=True, null=True)  # Field name made lowercase.
    user = models.ForeignKey('UsersCustomuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'indexer_gscverify'


class IndexerIndexapi(models.Model):
    id = models.BigIntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)
    email = models.CharField(max_length=200)
    indexapi = models.JSONField(db_column='indexApi')  # Field name made lowercase.
    user = models.ForeignKey('UsersCustomuser', models.DO_NOTHING)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'indexer_indexapi'


class IndexerPages(models.Model):
    id = models.BigIntegerField(primary_key=True)
    web_id = models.IntegerField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    index_status = models.SmallIntegerField(blank=True, null=True)
    indexed_date = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    date_tracking = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    rank = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'indexer_pages'


class IndexerSitemap(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    website = models.CharField(max_length=200)
    results = models.TextField(blank=True, null=True)
    user = models.ForeignKey('UsersCustomuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'indexer_sitemap'


class IndexerUrlshortner(models.Model):
    id = models.BigAutoField(primary_key=True)
    updated_at = models.DateTimeField()
    pages = models.TextField(blank=True, null=True)
    jsonfile = models.TextField(db_column='jsonFile', blank=True, null=True)  # Field name made lowercase.
    jsonresponse = models.TextField(db_column='JsonResponse', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField()
    gscverify = models.ForeignKey(IndexerGscverify, models.DO_NOTHING, db_column='GSCVerify_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'indexer_urlshortner'


class IndexerWebsite(models.Model):
    id = models.BigIntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)
    website = models.CharField(max_length=200)
    pages = models.TextField(blank=True, null=True)
    jsonfile = models.TextField(db_column='jsonFile', blank=True, null=True)  # Field name made lowercase.
    indexapi = models.ForeignKey(IndexerIndexapi, models.DO_NOTHING)
    jsonresponse = models.TextField(db_column='JsonResponse', blank=True, null=True)  # Field name made lowercase.
    times_indexed = models.IntegerField(blank=True, null=True)
    check_index = models.BooleanField()
    index_now = models.BooleanField()
    indexedrate = models.IntegerField(db_column='indexedRate', blank=True, null=True)  # Field name made lowercase.
    times_indexedrate = models.IntegerField(db_column='times_indexedRate', blank=True, null=True)  # Field name made lowercase.
    nonindexedpages = models.TextField(db_column='NonindexedPages', blank=True, null=True)  # Field name made lowercase.
    runindexer5 = models.BooleanField(db_column='RunIndexer5')  # Field name made lowercase.
    disableindexing = models.BooleanField(db_column='disableIndexing')  # Field name made lowercase.
    indexedpages = models.TextField(db_column='indexedPages', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'indexer_website'


class PegasusEmployeesEmployee(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=20)
    salary = models.IntegerField()
    user = models.ForeignKey('UsersCustomuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'pegasus_employees_employee'


class PegasusExamplesPayment(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    id = models.UUIDField(primary_key=True)
    charge_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    amount = models.IntegerField()
    user = models.ForeignKey('UsersCustomuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'pegasus_examples_payment'


class RestFrameworkApiKeyApikey(models.Model):
    id = models.CharField(primary_key=True, max_length=150)
    created = models.DateTimeField()
    name = models.CharField(max_length=50)
    revoked = models.BooleanField()
    expiry_date = models.DateTimeField(blank=True, null=True)
    hashed_key = models.CharField(max_length=150)
    prefix = models.CharField(unique=True, max_length=8)

    class Meta:
        managed = False
        db_table = 'rest_framework_api_key_apikey'


class SocialaccountSocialaccount(models.Model):
    provider = models.CharField(max_length=30)
    uid = models.CharField(max_length=191)
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()
    extra_data = models.TextField()
    user = models.ForeignKey('UsersCustomuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialaccount'
        unique_together = (('provider', 'uid'),)


class SocialaccountSocialapp(models.Model):
    provider = models.CharField(max_length=30)
    name = models.CharField(max_length=40)
    client_id = models.CharField(max_length=191)
    secret = models.CharField(max_length=191)
    key = models.CharField(max_length=191)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialapp'


class SocialaccountSocialappSites(models.Model):
    socialapp = models.ForeignKey(SocialaccountSocialapp, models.DO_NOTHING)
    site = models.ForeignKey(DjangoSite, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialapp_sites'
        unique_together = (('socialapp', 'site'),)


class SocialaccountSocialtoken(models.Model):
    token = models.TextField()
    token_secret = models.TextField()
    expires_at = models.DateTimeField(blank=True, null=True)
    account = models.ForeignKey(SocialaccountSocialaccount, models.DO_NOTHING)
    app = models.ForeignKey(SocialaccountSocialapp, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialtoken'
        unique_together = (('app', 'account'),)


class TaggitTag(models.Model):
    name = models.CharField(unique=True, max_length=100)
    slug = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'taggit_tag'


class TaggitTaggeditem(models.Model):
    object_id = models.IntegerField()
    content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING)
    tag = models.ForeignKey(TaggitTag, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'taggit_taggeditem'
        unique_together = (('content_type', 'object_id', 'tag'),)


class TblLoghistory(models.Model):
    id = models.IntegerField(primary_key=True)
    descriptions = models.TextField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    datetime_added = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_loghistory'


class TeamsExamplePlayer(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(max_length=100)
    sex = models.CharField(max_length=10)
    date_of_birth = models.DateField(blank=True, null=True)
    team = models.ForeignKey('TeamsTeam', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'teams_example_player'


class TeamsInvitation(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    id = models.UUIDField(primary_key=True)
    email = models.CharField(max_length=254)
    role = models.CharField(max_length=100)
    is_accepted = models.BooleanField()
    accepted_by = models.ForeignKey('UsersCustomuser', models.DO_NOTHING, blank=True, null=True)
    invited_by = models.ForeignKey('UsersCustomuser', models.DO_NOTHING)
    team = models.ForeignKey('TeamsTeam', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'teams_invitation'


class TeamsMembership(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    role = models.CharField(max_length=100)
    team = models.ForeignKey('TeamsTeam', models.DO_NOTHING)
    user = models.ForeignKey('UsersCustomuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'teams_membership'


class TeamsTeam(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(max_length=100)
    slug = models.CharField(unique=True, max_length=50)
    billing_details_last_changed = models.DateTimeField()
    last_synced_with_stripe = models.DateTimeField(blank=True, null=True)
    subscription = models.ForeignKey(DjstripeSubscription, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teams_team'


class UsersCustomuser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    avatar = models.CharField(max_length=100)
    customer = models.ForeignKey(DjstripeCustomer, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_customuser'


class UsersCustomuserGroups(models.Model):
    customuser = models.ForeignKey(UsersCustomuser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_customuser_groups'
        unique_together = (('customuser', 'group'),)


class UsersCustomuserUserPermissions(models.Model):
    customuser = models.ForeignKey(UsersCustomuser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_customuser_user_permissions'
        unique_together = (('customuser', 'permission'),)


class WagtailadminAdmin(models.Model):

    class Meta:
        managed = False
        db_table = 'wagtailadmin_admin'


class WagtailcoreCollection(models.Model):
    path = models.CharField(unique=True, max_length=255, db_collation='C')
    depth = models.IntegerField()
    numchild = models.IntegerField()
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'wagtailcore_collection'


class WagtailcoreCollectionviewrestriction(models.Model):
    restriction_type = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    collection = models.ForeignKey(WagtailcoreCollection, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'wagtailcore_collectionviewrestriction'


class WagtailcoreCollectionviewrestrictionGroups(models.Model):
    collectionviewrestriction = models.ForeignKey(WagtailcoreCollectionviewrestriction, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'wagtailcore_collectionviewrestriction_groups'
        unique_together = (('collectionviewrestriction', 'group'),)


class WagtailcoreComment(models.Model):
    text = models.TextField()
    contentpath = models.TextField()
    position = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    resolved_at = models.DateTimeField(blank=True, null=True)
    page = models.ForeignKey('WagtailcorePage', models.DO_NOTHING)
    resolved_by = models.ForeignKey(UsersCustomuser, models.DO_NOTHING, blank=True, null=True)
    revision_created = models.ForeignKey('WagtailcorePagerevision', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(UsersCustomuser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'wagtailcore_comment'


class WagtailcoreCommentreply(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    comment = models.ForeignKey(WagtailcoreComment, models.DO_NOTHING)
    user = models.ForeignKey(UsersCustomuser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'wagtailcore_commentreply'


class WagtailcoreGroupapprovaltask(models.Model):
    task_ptr = models.OneToOneField('WagtailcoreTask', models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'wagtailcore_groupapprovaltask'


class WagtailcoreGroupapprovaltaskGroups(models.Model):
    groupapprovaltask = models.ForeignKey(WagtailcoreGroupapprovaltask, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'wagtailcore_groupapprovaltask_groups'
        unique_together = (('groupapprovaltask', 'group'),)


class WagtailcoreGroupcollectionpermission(models.Model):
    collection = models.ForeignKey(WagtailcoreCollection, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'wagtailcore_groupcollectionpermission'
        unique_together = (('group', 'collection', 'permission'),)


class WagtailcoreGrouppagepermission(models.Model):
    permission_type = models.CharField(max_length=20)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    page = models.ForeignKey('WagtailcorePage', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'wagtailcore_grouppagepermission'
        unique_together = (('group', 'page', 'permission_type'),)


class WagtailcoreLocale(models.Model):
    language_code = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'wagtailcore_locale'


class WagtailcoreModellogentry(models.Model):
    label = models.TextField()
    action = models.CharField(max_length=255)
    data = models.JSONField()
    timestamp = models.DateTimeField()
    content_changed = models.BooleanField()
    deleted = models.BooleanField()
    object_id = models.CharField(max_length=255)
    content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING, blank=True, null=True)
    user_id = models.BigIntegerField(blank=True, null=True)
    uuid = models.UUIDField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wagtailcore_modellogentry'


class WagtailcorePage(models.Model):
    path = models.CharField(unique=True, max_length=255, db_collation='C')
    depth = models.IntegerField()
    numchild = models.IntegerField()
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    live = models.BooleanField()
    has_unpublished_changes = models.BooleanField()
    url_path = models.TextField()
    seo_title = models.CharField(max_length=255)
    show_in_menus = models.BooleanField()
    search_description = models.TextField()
    go_live_at = models.DateTimeField(blank=True, null=True)
    expire_at = models.DateTimeField(blank=True, null=True)
    expired = models.BooleanField()
    content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING)
    owner = models.ForeignKey(UsersCustomuser, models.DO_NOTHING, blank=True, null=True)
    locked = models.BooleanField()
    latest_revision_created_at = models.DateTimeField(blank=True, null=True)
    first_published_at = models.DateTimeField(blank=True, null=True)
    live_revision = models.ForeignKey('WagtailcorePagerevision', models.DO_NOTHING, blank=True, null=True)
    last_published_at = models.DateTimeField(blank=True, null=True)
    draft_title = models.CharField(max_length=255)
    locked_at = models.DateTimeField(blank=True, null=True)
    locked_by = models.ForeignKey(UsersCustomuser, models.DO_NOTHING, blank=True, null=True)
    translation_key = models.UUIDField()
    locale = models.ForeignKey(WagtailcoreLocale, models.DO_NOTHING)
    alias_of = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wagtailcore_page'
        unique_together = (('translation_key', 'locale'),)


class WagtailcorePagelogentry(models.Model):
    label = models.TextField()
    action = models.CharField(max_length=255)
    data = models.JSONField()
    timestamp = models.DateTimeField()
    content_changed = models.BooleanField()
    deleted = models.BooleanField()
    content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING, blank=True, null=True)
    page_id = models.IntegerField()
    revision_id = models.IntegerField(blank=True, null=True)
    user_id = models.BigIntegerField(blank=True, null=True)
    uuid = models.UUIDField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wagtailcore_pagelogentry'


class WagtailcorePagerevision(models.Model):
    submitted_for_moderation = models.BooleanField()
    created_at = models.DateTimeField()
    content = models.JSONField()
    approved_go_live_at = models.DateTimeField(blank=True, null=True)
    page = models.ForeignKey(WagtailcorePage, models.DO_NOTHING)
    user = models.ForeignKey(UsersCustomuser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wagtailcore_pagerevision'


class WagtailcorePagesubscription(models.Model):
    comment_notifications = models.BooleanField()
    page = models.ForeignKey(WagtailcorePage, models.DO_NOTHING)
    user = models.ForeignKey(UsersCustomuser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'wagtailcore_pagesubscription'
        unique_together = (('page', 'user'),)


class WagtailcorePageviewrestriction(models.Model):
    password = models.CharField(max_length=255)
    page = models.ForeignKey(WagtailcorePage, models.DO_NOTHING)
    restriction_type = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'wagtailcore_pageviewrestriction'


class WagtailcorePageviewrestrictionGroups(models.Model):
    pageviewrestriction = models.ForeignKey(WagtailcorePageviewrestriction, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'wagtailcore_pageviewrestriction_groups'
        unique_together = (('pageviewrestriction', 'group'),)


class WagtailcoreSite(models.Model):
    hostname = models.CharField(max_length=255)
    port = models.IntegerField()
    is_default_site = models.BooleanField()
    root_page = models.ForeignKey(WagtailcorePage, models.DO_NOTHING)
    site_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'wagtailcore_site'
        unique_together = (('hostname', 'port'),)


class WagtailcoreTask(models.Model):
    name = models.CharField(max_length=255)
    active = models.BooleanField()
    content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'wagtailcore_task'


class WagtailcoreTaskstate(models.Model):
    status = models.CharField(max_length=50)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField(blank=True, null=True)
    content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING)
    page_revision = models.ForeignKey(WagtailcorePagerevision, models.DO_NOTHING)
    task = models.ForeignKey(WagtailcoreTask, models.DO_NOTHING)
    workflow_state = models.ForeignKey('WagtailcoreWorkflowstate', models.DO_NOTHING)
    finished_by = models.ForeignKey(UsersCustomuser, models.DO_NOTHING, blank=True, null=True)
    comment = models.TextField()

    class Meta:
        managed = False
        db_table = 'wagtailcore_taskstate'


class WagtailcoreWorkflow(models.Model):
    name = models.CharField(max_length=255)
    active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'wagtailcore_workflow'


class WagtailcoreWorkflowpage(models.Model):
    page = models.OneToOneField(WagtailcorePage, models.DO_NOTHING, primary_key=True)
    workflow = models.ForeignKey(WagtailcoreWorkflow, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'wagtailcore_workflowpage'


class WagtailcoreWorkflowstate(models.Model):
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    current_task_state = models.OneToOneField(WagtailcoreTaskstate, models.DO_NOTHING, blank=True, null=True)
    page = models.OneToOneField(WagtailcorePage, models.DO_NOTHING)
    requested_by = models.ForeignKey(UsersCustomuser, models.DO_NOTHING, blank=True, null=True)
    workflow = models.ForeignKey(WagtailcoreWorkflow, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'wagtailcore_workflowstate'


class WagtailcoreWorkflowtask(models.Model):
    sort_order = models.IntegerField(blank=True, null=True)
    task = models.ForeignKey(WagtailcoreTask, models.DO_NOTHING)
    workflow = models.ForeignKey(WagtailcoreWorkflow, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'wagtailcore_workflowtask'
        unique_together = (('workflow', 'task'),)


class WagtaildocsDocument(models.Model):
    title = models.CharField(max_length=255)
    file = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    uploaded_by_user = models.ForeignKey(UsersCustomuser, models.DO_NOTHING, blank=True, null=True)
    collection = models.ForeignKey(WagtailcoreCollection, models.DO_NOTHING)
    file_size = models.IntegerField(blank=True, null=True)
    file_hash = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'wagtaildocs_document'


class WagtaildocsUploadeddocument(models.Model):
    file = models.CharField(max_length=200)
    uploaded_by_user = models.ForeignKey(UsersCustomuser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wagtaildocs_uploadeddocument'


class WagtailembedsEmbed(models.Model):
    url = models.TextField()
    max_width = models.SmallIntegerField(blank=True, null=True)
    type = models.CharField(max_length=10)
    html = models.TextField()
    title = models.TextField()
    author_name = models.TextField()
    provider_name = models.TextField()
    thumbnail_url = models.TextField()
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    last_updated = models.DateTimeField()
    hash = models.CharField(unique=True, max_length=32)
    cache_until = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wagtailembeds_embed'


class WagtailformsFormsubmission(models.Model):
    form_data = models.JSONField()
    submit_time = models.DateTimeField()
    page = models.ForeignKey(WagtailcorePage, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'wagtailforms_formsubmission'


class WagtailimagesImage(models.Model):
    title = models.CharField(max_length=255)
    file = models.CharField(max_length=100)
    width = models.IntegerField()
    height = models.IntegerField()
    created_at = models.DateTimeField()
    focal_point_x = models.IntegerField(blank=True, null=True)
    focal_point_y = models.IntegerField(blank=True, null=True)
    focal_point_width = models.IntegerField(blank=True, null=True)
    focal_point_height = models.IntegerField(blank=True, null=True)
    uploaded_by_user = models.ForeignKey(UsersCustomuser, models.DO_NOTHING, blank=True, null=True)
    file_size = models.IntegerField(blank=True, null=True)
    collection = models.ForeignKey(WagtailcoreCollection, models.DO_NOTHING)
    file_hash = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'wagtailimages_image'


class WagtailimagesRendition(models.Model):
    file = models.CharField(max_length=100)
    width = models.IntegerField()
    height = models.IntegerField()
    focal_point_key = models.CharField(max_length=16)
    filter_spec = models.CharField(max_length=255)
    image = models.ForeignKey(WagtailimagesImage, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'wagtailimages_rendition'
        unique_together = (('image', 'filter_spec', 'focal_point_key'),)


class WagtailimagesUploadedimage(models.Model):
    file = models.CharField(max_length=200)
    uploaded_by_user = models.ForeignKey(UsersCustomuser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wagtailimages_uploadedimage'


class WagtailredirectsRedirect(models.Model):
    old_path = models.CharField(max_length=255)
    is_permanent = models.BooleanField()
    redirect_link = models.CharField(max_length=255)
    redirect_page = models.ForeignKey(WagtailcorePage, models.DO_NOTHING, blank=True, null=True)
    site = models.ForeignKey(WagtailcoreSite, models.DO_NOTHING, blank=True, null=True)
    automatically_created = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    redirect_page_route_path = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'wagtailredirects_redirect'
        unique_together = (('old_path', 'site'),)


class WagtailsearchEditorspick(models.Model):
    sort_order = models.IntegerField(blank=True, null=True)
    description = models.TextField()
    page = models.ForeignKey(WagtailcorePage, models.DO_NOTHING)
    query = models.ForeignKey('WagtailsearchQuery', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'wagtailsearch_editorspick'


class WagtailsearchIndexentry(models.Model):
    object_id = models.CharField(max_length=50)
    title_norm = models.FloatField()
    content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING)
    autocomplete = models.TextField()  # This field type is a guess.
    title = models.TextField()  # This field type is a guess.
    body = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'wagtailsearch_indexentry'
        unique_together = (('content_type', 'object_id'),)


class WagtailsearchQuery(models.Model):
    query_string = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'wagtailsearch_query'


class WagtailsearchQuerydailyhits(models.Model):
    date = models.DateField()
    hits = models.IntegerField()
    query = models.ForeignKey(WagtailsearchQuery, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'wagtailsearch_querydailyhits'
        unique_together = (('query', 'date'),)


class WagtailusersUserprofile(models.Model):
    submitted_notifications = models.BooleanField()
    approved_notifications = models.BooleanField()
    rejected_notifications = models.BooleanField()
    user = models.OneToOneField(UsersCustomuser, models.DO_NOTHING)
    preferred_language = models.CharField(max_length=10)
    current_time_zone = models.CharField(max_length=40)
    avatar = models.CharField(max_length=100)
    updated_comments_notifications = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'wagtailusers_userprofile'
