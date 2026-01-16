from django.apps import AppConfig


class SettingsConfig(AppConfig):
    default_auto_field: str = 'django.db.models.BigAutoField' # type: ignore
    name = 'settings'
    label = 'user_settings' # type: ignore
