from django.urls import path
from . import views

urlpatterns = [
    path('', views.server, name='server'),
    path('<int:pk>', views.serverdetail, name='serverdetail'),
    path('cpu/<int:server_pk>', views.cpuinfo, name='cpuinfo'),
]