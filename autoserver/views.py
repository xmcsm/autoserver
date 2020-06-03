from django.shortcuts import render
from django.db.models import Count
from respository import models

# Create your views here.
def index(request):
    context = {}
    servers = models.Server.objects.all().values('os_platform').annotate(platformNum=Count("os_platform"))
    server_list = []
    for server in servers:
        servercount = {}
        servercount['os_platform'] = server['os_platform']
        servercount['platformNum'] = server['platformNum']
        server_list.append(servercount)
    context['server_list'] = server_list
    return render(request,'index.html',context)