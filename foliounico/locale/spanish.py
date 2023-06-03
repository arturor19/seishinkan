# coding=utf-8
from django.utils.translation import gettext_lazy as _

# Override default permission labels with Spanish translations
_('Can add %(verbose_name)s').replace('Can add', 'Puede agregar')
_('Can change %(verbose_name)s').replace('Can change', 'Puede cambiar')
_('Can delete %(verbose_name)s').replace('Can delete', 'Puede eliminar')
_('Can view %(verbose_name)s').replace('Can view', 'Puede ver')