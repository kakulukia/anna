from django.apps import AppConfig
from django.db.models.signals import pre_save


class ApplicationConfig(AppConfig):
    name = "application"
    verbose_name = "Anwendung"

    def ready(self):
        from users.models import User

        from . import signals

        pre_save.connect(signals.update_last_login, sender=User)
