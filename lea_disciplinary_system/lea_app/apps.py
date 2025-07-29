from django.apps import AppConfig

class LeaAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lea_app'

    def ready(self):
        import lea_app.signals  # to connect signals
