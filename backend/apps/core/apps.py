import sys

from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"
    verbose_name = "Core & Infrastructure"

    def ready(self):
        # Python 3.14 compatibility patch for Django template context copying.
        if sys.version_info >= (3, 14):
            import django.template.context as dtc

            def _patch_base_context_copy(self):
                cls = self.__class__
                duplicate = cls.__new__(cls)
                duplicate.__dict__.update(self.__dict__)
                duplicate.dicts = self.dicts[:]
                return duplicate

            dtc.BaseContext.__copy__ = _patch_base_context_copy
