from django.apps import AppConfig


class AppNameConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.apps.app_name"
    label = "app_name"
    verbose_name = "app_name"
