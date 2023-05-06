import ssl

from .settings import *

SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)
REDIS_URL = f"{os.environ.get('REDIS_URL', 'redis://localhost:6379/0')}?ssl_cert_reqs=none"
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
BROKER_USE_SSL = {
    'ssl_cert_reqs': ssl.CERT_NONE
}

DEBUG = env.bool("DJANGO_DEBUG", True)


# fix ssl mixed content issues
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# update with your site/domain
ALLOWED_HOSTS = [
    '*'
]


DATABASES = {
    "default": env.db("DATABASE_URL")
}

DATABASES["default"]["ATOMIC_REQUESTS"] = True
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)


USE_HTTPS_IN_ABSOLUTE_URLS = True

# use whitenoise for staticfiles
MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

REDIS_URL = os.environ.get("REDIS_URL")  # from docker compose file

if REDIS_URL:
    CACHES = {
        "default": env.cache('REDIS_URL')
    }

# Celery Settings
try:
    from kombu import Queue
    from celery import Celery
    CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='amqp://localhost')
    if CELERY_BROKER_URL:
        CELERYD_TASK_SOFT_TIME_LIMIT = 60
        CELERY_ACCEPT_CONTENT = ['application/json']
        CELERY_TASK_SERIALIZER = 'json'
        CELERY_RESULT_SERIALIZER = 'json'
        CELERY_RESULT_BACKEND = env('REDIS_URL', default='redis://localhost:6379/0')
        CELERY_DEFAULT_QUEUE = 'default'
        CELERY_CACHE_BACKEND = 'django-cache'
        CELERY_RESULT_BACKEND_DB = 'postgresql://..'
        CELERY_QUEUES = (
            Queue('default'),
        )
        CELERY_CREATE_MISSING_QUEUES = True
except ModuleNotFoundError:
    print("Celery/kombu not installed. Skipping...")


# Static And Media Settings
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME', default=None)
if AWS_STORAGE_BUCKET_NAME:
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_CUSTOM_DOMAIN = env('AWS_S3_CUSTOM_DOMAIN', default=None) or f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=600'}

    # s3 static settings
    STATIC_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
    STATICFILES_STORAGE = 'tutorial.storages.StaticStorage'

    # s3 public media settings
    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'tutorial.storages.PublicMediaStorage'
else:
    MIDDLEWARE.insert(2, 'whitenoise.middleware.WhiteNoiseMiddleware')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
    WHITENOISE_USE_FINDERS = True
    STATIC_HOST = env('DJANGO_STATIC_HOST', default='')
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATIC_URL = STATIC_HOST + '/static/'
    if DEBUG:
        WHITENOISE_AUTOREFRESH = True