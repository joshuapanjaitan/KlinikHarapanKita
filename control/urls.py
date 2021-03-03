from django.urls import path, re_path
from . import views
urlpatterns = [
    path('', views.control, name='control'),
    path('call/', views.call, name='call'),
    re_path(r'^detail/(?P<code>[A-Z]+)$', views.detail, name='detail'),
]
