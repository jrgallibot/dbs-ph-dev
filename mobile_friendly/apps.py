from django.apps import AppConfig


class MobileFriendlyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mobile_friendly'

    def ready(self):
        from jobs import updater
        updater.start()

