# from django.contrib import admin
# from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import HomePageView
from .views import signup


urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('signup/', signup, name='signup'),
 #   path('es-mx/admin/logout/', admin_site.logout, name='admin_logout'),  # Ruta personalizada para cerrar sesión
 #   path('es-mx/admin/', admin_site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
