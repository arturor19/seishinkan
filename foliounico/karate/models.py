# Create your models here.
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .enums import Cintas
from .enums import Rol
from .managers import CustomUserManager


class ShortUUIDField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 8
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None)
        if not value:
            value = str(uuid.uuid4())[:8]
            setattr(model_instance, self.attname, value)
        return value


class Dojo(models.Model):
    nombre_dojo = models.CharField(max_length=50, help_text="Nombre del dojo")
    calle = models.CharField(max_length=50, help_text="Calle")
    numero_exterior = models.CharField(max_length=15, help_text="Calle", verbose_name="Numero exterior")
    numero_interior = models.CharField(max_length=15, help_text="Calle", verbose_name="Numero interior", blank=True,
                                       null=True)
    colonia = models.CharField(max_length=50, help_text="Colonia", blank=True, null=True)
    codigo_postal = models.IntegerField()
    ciudad = models.CharField(max_length=50, help_text="Ciudad")
    estado = models.CharField(max_length=50, help_text="Estado")
    ubicacion_maps = models.URLField(max_length=200, verbose_name="Link ubicación maps")

    def __str__(self):
        return f"{self.nombre_dojo}"


class CodigoResgistro(models.Model):
    id = ShortUUIDField(unique=True, primary_key=True, editable=False)
    dojo = models.ForeignKey(Dojo, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=Rol.choices, default=Rol.ALUMNO)


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    fecha_de_nacimiento = models.DateField(null=True, blank=True)
    estatura = models.DecimalField(decimal_places=2, max_digits=12, null=True, blank=True)
    peso = models.DecimalField(decimal_places=2, max_digits=12, null=True, blank=True)
    rol = models.CharField(max_length=20, choices=Rol.choices, default=Rol.ALUMNO)
    cinta = models.CharField(max_length=20, choices=Cintas.choices, default=Cintas.BLANCA)
    dojo = models.ForeignKey(Dojo, on_delete=models.CASCADE, null=True, blank=True)
    nombre_completo = models.CharField(max_length=255, blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=True,
        help_text=_("Designa si el usuario puede iniciar sesión en el sitio de administración."),
    )
    numero_telefono = models.CharField(max_length=10, verbose_name="Número de teléfono")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Remove 'username' from REQUIRED_FIELDS

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.username:  # Generate username only if it doesn't exist
            self.username = self.generate_username()
        self.nombre_completo = f"{self.first_name} {self.last_name}"
        super().save(*args, **kwargs)

    def generate_username(self):
        username = f"{self.first_name.lower()}.{self.last_name.lower()}".replace(" ", "")
        count = 1
        while CustomUser.objects.filter(username=username).exists():
            # If the username already exists, append a count to make it unique
            count += 1
            username = f"{self.first_name.lower()}.{self.last_name.lower()}.{count}".replace(" ", "")
        return username

    def __str__(self):
        return f"{self.nombre_completo} ({self.email})"


class Torneo(models.Model):
    class Meta:
        verbose_name_plural = "Torneos"
        unique_together = ('nombre_del_torneo', 'fecha_del_torneo')

    nombre_del_torneo = models.CharField(max_length=50, help_text="Nombre del torneo")
    fecha_del_torneo = models.DateTimeField()
    direccion = models.CharField(max_length=200, help_text="Dirección")
    ubicacion_maps = models.URLField(max_length=200, verbose_name="Link ubicación maps")

    def __str__(self):
        return f"{self.nombre_del_torneo} ({self.fecha_del_torneo})"


class ResgistroTorneo(models.Model):
    class Meta:
        verbose_name_plural = "Registro de Torneos"
        unique_together = ('Torneo', 'Alumno')

    Torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE)
    Alumno = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Examen(models.Model):
    class Meta:
        verbose_name_plural = "Exámenes"
        unique_together = ('fecha_del_examen', 'grado_seguir', 'grado_actual')

    nombre_del_examen = models.CharField(max_length=50, help_text="Nombre del exámen")
    fecha_del_examen = models.DateTimeField()
    grado_actual = models.CharField(max_length=20, choices=Cintas.choices, default=Cintas.BLANCA)
    grado_seguir = models.CharField(max_length=20, choices=Cintas.choices, default=Cintas.BLANCA,
                                    help_text="Grado a seguir")
    direccion = models.CharField(max_length=200, help_text="Dirección")
    ubicacion_maps = models.URLField(max_length=200, verbose_name="Link ubicación maps")

    def __str__(self):
        return f"{self.nombre_del_examen} ({self.fecha_del_examen})"


class ResgistroExamen(models.Model):
    class Meta:
        verbose_name_plural = "Registro de Examen"
        unique_together = ('Examen', 'Alumno')

    Examen = models.ForeignKey(Examen, on_delete=models.CASCADE)
    Alumno = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    Calificacion = models.DecimalField(decimal_places=2, null=True, blank=True, help_text="Calificación", max_digits=4)
