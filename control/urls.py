from django.urls import path, re_path
from . import views
urlpatterns = [
    path('', views.control, name='control'),
    path('call/', views.call, name='call'),
    re_path(r'^detail/(?P<code>[A-Z]+)$', views.detail, name='detail'),
    re_path(
        r'^skip/(?P<layanan>[A-Z]+)/(?P<queue>[0-9]+)$', views.skip, name='skip'),
    re_path(
        r'^finish/(?P<layanan>[A-Z]+)/(?P<queue>[\w-]+)$', views.finish, name='finish'),
]
