from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
import json
from .charts import LineCharts,MutiplePieCharts,BarCharts
from respository import models

# Create your views here.
def login(request):
    return render(request,'login.html')


def server(request):
    context = {}
    servers = models.Server.objects.exclude(device_status_id=2)
    context['servers'] = servers
    return render(request,'server.html',context)

def bakcserver(request):
    context = {}
    servers = models.Server.objects.exclude(device_status_id=1)
    context['servers'] = servers
    return render(request,'back_server.html',context)

def serverdetail(request,pk,type):
    context = {}
    server = models.Server.objects.get(pk=pk)
    nets = models.Net.objects.filter(server_id=pk)
    context['server'] = server
    context['nets'] = nets
    context['type'] = type
    return render(request,'serverDetail.html',context)

def GetCpu(request,server_pk):
    print(server_pk)
    cpus = models.Cpu.objects.filter(server_id=server_pk)
    print(cpus)
    data = []
    cpudata = []
    for cpu in cpus:
        cpudata.append([cpu.create_time.strftime('%Y-%m-%d %H:%M:%S'), cpu.percent_avg])
    data.append('CPU')
    data.append(cpudata)

    linechart = LineCharts(data)

    data = {}
    data['status'] = 'SUCCESS'
    data['data'] = linechart
    return JsonResponse(data)

def GetMem(request,server_pk):
    data = []

    mems = models.Mem.objects.filter(server_id=server_pk)
    memdata = []
    for mem in mems:
        memdata.append([mem.create_time.strftime('%Y-%m-%d %H:%M:%S'), mem.percent])

    data.append('内存')
    data.append(memdata)
    linechart = LineCharts(data)

    data = {}
    data['status'] = 'SUCCESS'
    data['data'] = linechart
    return JsonResponse(data)

def GetSwap(request,server_pk):
    data = []
    swaps = models.Swap.objects.filter(server_id=server_pk)
    swapdata = []
    for swap in swaps:
        swapdata.append([swap.create_time.strftime('%Y-%m-%d %H:%M:%S'), swap.percent])

    data.append('Swap')
    data.append(swapdata)
    linechart = LineCharts(data)

    data = {}
    data['status'] = 'SUCCESS'
    data['data'] = linechart
    return JsonResponse(data)

def GetDisk(request,server_pk):

    disks = models.Disk.objects.filter(server_id=server_pk)
    diskdata = []
    for disk in disks:
        diskdetail = models.DiskDetail.objects.filter(disk=disk).order_by('-create_time').first()
        detail_list = []
        detail_list.append(['已使用',float('%.2f' % float(diskdetail.percent))])
        detail_list.append(['空闲', float('%.2f' % (100 - float(diskdetail.percent)))])
        diskdata.append([disk.mountpoint,detail_list])
    piechart = MutiplePieCharts(diskdata)
    data = {}
    data['status'] = 'SUCCESS'
    data['data'] = piechart
    return JsonResponse(data)

def GetNet(request,server_pk):
    data = []
    nets = models.Net.objects.filter(server_id=server_pk)
    bytes_sent_list = []
    bytes_recv_list = []
    packets_sent_list = []
    packets_recv_list = []
    x_list = []
    for net in nets:
        x_list.append(net.address)
        bytes_sent_list.append(net.bytes_sent)
        bytes_recv_list.append(net.bytes_recv)
        packets_sent_list.append(net.packets_sent)
        packets_recv_list.append(net.packets_recv)

    data.append('网卡IO信息')
    data.append(x_list)
    data.append([['已发送字节数',bytes_sent_list],['已接收字节数',bytes_recv_list],['已发送包数',packets_sent_list],['已接收包数',packets_recv_list]])

    barcharts = BarCharts(data)
    data = {}
    data['status'] = 'SUCCESS'
    data['data'] = barcharts
    return JsonResponse(data)


