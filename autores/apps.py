from django.apps import AppConfig

class AutoresConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'autores'

    def ready(self, *args, **kwargs) -> None:
        import autores.signals #noqa
        super_ready = super().ready(*args, **kwargs)
        return super_ready
