from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('layanan/', include(('layanan.urls', 'layanan'), namespace='layanan')),
    path('control/', include(('control.urls', 'control'), namespace='control')),
]
