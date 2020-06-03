from django.shortcuts import render,HttpResponse
import json
from .charts import LineCharts
from respository import models

# Create your views here.
def login(request):
    return render(request,'login.html')


def server(request):
    context = {}
    servers = models.Server.objects.all()
    context['servers'] = servers
    return render(request,'server.html',context)

def serverdetail(request,pk):
    context = {}

    cpus = models.Cpu.objects.filter(server_id=pk)
    cpudata = []
    for cpu in cpus:
        cpudata.append([cpu.create_time.strftime('%y-%m-%d %H:%M:%S'),cpu.percent_avg])


    mems = models.Mem.objects.filter(server_id=pk)
    memdata = []
    for mem in mems:
        memdata.append([mem.create_time.strftime('%y-%m-%d %H:%M:%S'), mem.percent])

    linechart = LineCharts(cpudata,memdata)
    server = models.Server.objects.get(pk=pk)
    context['server'] = server
    context['linechart'] = linechart
    return render(request,'serverDetail.html',context)

def cpuinfo(request,server_pk):

    return HttpResponse('')


