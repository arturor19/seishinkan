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
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
