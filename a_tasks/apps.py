from django.apps import AppConfig


class ATasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'a_tasks'

    def ready(self):
        # Import and register the defined signals
        import a_tasks.signals  # noqa
