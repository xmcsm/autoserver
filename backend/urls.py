from django.urls import path
from . import views

urlpatterns = [
    path('', views.server, name='server'),
    path('back/', views.bakcserver, name='bakcserver'),
    path('<int:pk>/<str:type>', views.serverdetail, name='serverdetail'),
    path('cpu/<int:server_pk>', views.GetCpu, name='getcpu'),
    path('mem/<int:server_pk>', views.GetMem, name='getmem'),
    path('swap/<int:server_pk>', views.GetSwap, name='getswap'),
    #path('disk/<int:server_pk>', views.GetDisk, name='getdisk'),
    path('net/<int:server_pk>', views.GetNetInfo, name='getnet'),
]