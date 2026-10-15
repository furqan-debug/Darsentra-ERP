"""Darsentra ERP Django Backend Configuration Package."""
import sys

# Python 3.14 compatibility patch for Django template context copying.
# In Python 3.14, copy(super()) copies the super proxy object rather than
# delegating to object.__copy__, causing AttributeError when setting duplicate.dicts.
if sys.version_info >= (3, 14):
    import django.template.context as _dtc

    def _patch_base_context_copy(self):
        cls = self.__class__
        duplicate = cls.__new__(cls)
        duplicate.__dict__.update(self.__dict__)
        duplicate.dicts = self.dicts[:]
        return duplicate

    _dtc.BaseContext.__copy__ = _patch_base_context_copy
