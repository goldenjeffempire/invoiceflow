from django.apps import AppConfig


class SettingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'settings'
    label = 'user_settings' # type: ignore
