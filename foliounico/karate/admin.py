# Register your models here.
from functools import wraps

from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from import_export.admin import ExportActionMixin

from .enums import Rol
from .forms import RegistroUsuarioForm
from .models import CodigoResgistro
from .models import CustomUser
from .models import Dojo
from .models import Examen
from .models import ResgistroExamen
from .models import ResgistroTorneo
from .models import Torneo

def restrict_access_to_role(view_func):
    @wraps(view_func)
    def _wrapped_view(self, request, *args, **kwargs):
        # Verificar si el usuario tiene el rol adecuado
        if request.user.is_authenticated and request.user.rol == Rol.ALUMNO:
            # Restringir el acceso si el usuario es un alumno
            return HttpResponseForbidden("Acceso denegado.")
        # Permitir acceso si el usuario tiene otros roles o no está autenticado
        return view_func(self, request, *args, **kwargs)
    return _wrapped_view

#class CustomLoginView(LoginView):
#    def get_success_url(self):
#        # Redirige a /es-mx/admin/ después del inicio de sesión
#        return reverse_lazy('admin:index')

# Registra la vista personalizada de inicio de sesión
#admin.site.login = CustomLoginView.as_view()


@admin.site.admin_view
def custom_logout(request):
    auth_logout(request)
    # Redirige a donde quieras después del cierre de sesión, por ejemplo, al login.
    return HttpResponseRedirect('/')  # Ajusta la redirección según tus necesidades


admin.site.logout = custom_logout

class RegistroUsuarioAdmin(BaseUserAdmin):
    form = RegistroUsuarioForm


@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Información Karate'), {'fields': ('fecha_de_nacimiento', 'numero_telefono', 'dojo', 'cinta', 'rol')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name',),
        }),
    )
    list_display = ['email', 'first_name', 'last_name', 'username', 'is_staff', "numero_telefono", 'dojo_nombre']
    search_fields = ('email', 'first_name', 'last_name', 'dojo__nombre_dojo')
    ordering = ('email',)

    def get_fieldsets(self, request, obj=None):
        if request.user.rol == Rol.SENSEI:
            return (
                (None, {'fields': ('email','password',)}),
                (_('Información Karate'), {'fields': ('fecha_de_nacimiento', 'numero_telefono', 'dojo', 'cinta', 'rol')}),
            )
        return super().get_fieldsets(request, obj=obj)
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Obtener el usuario actual
        current_user = request.user
        # Verificar si el usuario es un alumno
        if current_user.rol == Rol.ALUMNO:
            # Filtrar los registros por el usuario actual
            queryset = queryset.filter(id=current_user.id)
        elif current_user.rol == Rol.SENSEI:
            # Filtrar los registros por el usuario actual
            queryset = queryset.filter(dojo=current_user.dojo)
        elif current_user.rol == Rol.ADMINISTRADOR:
            # Obtener los registros
            queryset = queryset.all()
        elif current_user.is_superuser:
            queryset = queryset.all()
        return queryset


@admin.register(Dojo)
class DojoAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = [
        'nombre_dojo',
        'calle',
        'numero_exterior',
        'numero_interior',
        'colonia',
        'codigo_postal',
        'ciudad',
        'estado',
        'ubicacion_maps',
    ]


@admin.register(CodigoResgistro)
class ResitroDeCodigos(ExportActionMixin, admin.ModelAdmin):
    list_display = [
        'id',
        'dojo',
        'rol',
    ]

    list_filter = [
        'dojo',
        'rol',
    ]


@admin.register(Torneo)
class TorneoAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = [
        'nombre_del_torneo',
        'fecha_del_torneo',
    ]

    list_filter = [
        'nombre_del_torneo',
        'fecha_del_torneo',
    ]

    def fecha_del_torneo(self, obj):
        return obj.Torneo.fecha_del_torneo


@admin.register(ResgistroTorneo)
class RegistroTorneoAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = [
        'Alumno',
        'nombre_del_torneo',
        'lugar',
        'fecha_del_torneo',
    ]

    list_filter = [
        'Alumno',
        'Torneo__nombre_del_torneo',
        'Torneo__fecha_del_torneo',
    ]

    def nombre_del_torneo(self, obj):
        return obj.Torneo.nombre_del_torneo

    def fecha_del_torneo(self, obj):
        return obj.Torneo.fecha_del_torneo

    def lugar(self, obj):
        return obj.Torneo.ubicacion_maps

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Obtener el usuario actual
        current_user = request.user
        # Verificar si el usuario es un alumno
        if current_user.rol == Rol.ALUMNO:
            # Filtrar los registros por el usuario actual
            queryset = queryset.filter(Alumno=current_user)
        elif current_user.rol == Rol.SENSEI:
            # Filtrar los registros por el usuario actual
            queryset = queryset.filter(Alumno__dojo=current_user.dojo)
        elif current_user.rol == Rol.ADMINISTRADOR:
            # Obtener los registros
            queryset = queryset.all()
        return queryset

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "Alumno" and request.user.rol == Rol.SENSEI:
            # Obtener el usuario actual
            current_user = request.user

            # Filtrar los alumnos por el dojo del usuario actual
            kwargs["queryset"] = CustomUser.objects.filter(dojo=current_user.dojo)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


"""
para las notificaciones 
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        today = timezone.now().date()
        return queryset.filter(Torneo__fecha_del_torneo__gte=today)
"""


@admin.register(Examen)
class ExamenAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = [
        'nombre_del_examen',
        'fecha_del_examen',
        'grado_actual',
        'grado_seguir',
    ]

    list_filter = [
        'nombre_del_examen',
        'fecha_del_examen',
        'grado_seguir',
    ]


@admin.register(ResgistroExamen)
class RegsitroDeExamenAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = [
        'examen_nombre',
        'examen_fecha',  # Add a new entry for the field
        'Alumno',
    ]

    list_filter = ['Examen__nombre_del_examen', 'Examen__fecha_del_examen', 'Alumno__nombre_completo',
                   'Alumno__email', ]

    def examen_fecha(self, obj):
        return obj.Examen.fecha_del_examen

    def examen_nombre(self, obj):
        return obj.Examen.nombre_del_examen

    examen_fecha.short_description = 'Fecha del Examen'  # Set the column header name

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Obtener el usuario actual
        current_user = request.user
        # Verificar si el usuario es un alumno
        if current_user.rol == Rol.ALUMNO:
            # Filtrar los registros por el usuario actual
            queryset = queryset.filter(Alumno=current_user)
        # Filtrar los registros por dojo de acuerdo al sensei y alumnos considerando que resgistro de examen no tiene dojo
        elif current_user.rol == Rol.SENSEI:
            # Filtrar los registros por el usuario actual
            queryset = queryset.filter(Alumno__dojo=current_user.dojo)
        elif current_user.rol == Rol.ADMINISTRADOR:
            # Obtener los registros
            queryset = queryset.all()
        return queryset

    # crear un metodo para que el sensei  pueda crear y modificar los examenes de su dojo
    def save_model(self, request, obj, form, change):
        if request.user.rol == Rol.SENSEI:
            obj.dojo = request.user.dojo
        obj.save()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "Alumno" and request.user.rol == Rol.SENSEI:
            # Obtener el usuario actual
            current_user = request.user

            # Filtrar los alumnos por el dojo del usuario actual
            kwargs["queryset"] = CustomUser.objects.filter(dojo=current_user.dojo)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.site_header = "Seishinkan"
admin.site.site_title = "Portal de Seishinkan"
admin.site.index_title = "Bienvenidos al portal de Seishinkan"
