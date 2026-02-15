from django.apps import AppConfig


class AttributesConfig(AppConfig):
    name = 'apps.attributes'
    verbose_name = 'ویژگی‌ها'

    def ready(self):
        import apps.attributes.signals  # noqa: F401
