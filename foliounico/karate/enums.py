from django.db import models
from django.utils.translation import gettext_lazy as _


class Rol(models.TextChoices):
    SENSEI = "Sensei", _("Sensei")
    ALUMNO = "Alumno", _("Alumno")
    ADMINISTRADOR = "Administrador", _("Administrador")


class Cintas(models.TextChoices):
    BLANCA = "Blanca", _("Blanca")
    AMARILLA = "Amarilla", _("Amarilla")
    NARANJA = "Naranja", _("Naranja")
    AZUL = "Azul", _("Azul")
    MORADA = "Morada", _("Morada")
    VERDE = "Verde", _("Verde")
    ROJO = "Rojo", _("Rojo")
    CAFE = "Cafe", _("Cafe")
    MARRON = "Marron", _("Marron")
    NEGRA = "Negra", _("Negra")
