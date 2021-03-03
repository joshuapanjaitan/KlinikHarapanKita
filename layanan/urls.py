from django.urls import path, re_path
from . import views
urlpatterns = [
    path('', views.list, name='list'),
    re_path(r'^queue/(?P<q_id>[A-Z]+)$', views.queue, name='queue'),
]
