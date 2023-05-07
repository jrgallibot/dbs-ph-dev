import os
from celery import Celery
from celery.schedules import crontab
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Home.settings')

app = Celery('Home')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.

app.conf.redbeat_redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
app.autodiscover_tasks()
app.conf.broker_pool_limit = 1
app.conf.broker_heartbeat = None
app.conf.broker_connection_timeout = 30
app.conf.worker_prefetch_multiplier = 1
app.conf.timezone = 'UTC'


app.conf.beat_schedule = {
    'per_day_update_index_rate': {
        'task': 'per_day_update_index_rate',
        'schedule': crontab(minute="*/480")
    },
    # 'every_fourth_checking_index': {
    #     'task': 'every_fourth_checking_index',
    #     'schedule': crontab(minute="*/60")
    # },
}