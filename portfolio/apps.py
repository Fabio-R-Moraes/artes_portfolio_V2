from django.apps import AppConfig

class PortfolioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'portfolio'

    def ready(self, *args, **kwargs) -> None:
        import portfolio.signals #noqa
        super_ready = super().ready(*args, *kwargs)

        return super_ready