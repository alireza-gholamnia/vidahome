from django.apps import AppConfig


class ListingsConfig(AppConfig):
    name = 'apps.listings'
    verbose_name = 'آگهی‌ها'

    def ready(self):
        import apps.listings.signals  # noqa: F401
