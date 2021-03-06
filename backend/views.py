from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
import json,datetime
from .charts import LineCharts,MutiplePieCharts,BarCharts
from respository import models

# Create your views here.
def login(request):
    return render(request,'login.html')

def GetNet(server):
    data = {}
    nets = models.Net.objects.filter(server=server)
    bytes_sent_list = []
    bytes_recv_list = []
    packets_sent_list = []
    packets_recv_list = []
    x_list = []
    for net in nets:
        x_list.append(net.address)
        bytes_sent_list.append(int(net.bytes_sent))
        bytes_recv_list.append(int(net.bytes_recv))
        packets_sent_list.append(int(net.packets_sent))
        packets_recv_list.append(int(net.packets_recv))
    data['ipaddrs'] = x_list
    data['datas'] = [{'name':'已发送字节数','data':bytes_sent_list},{'name':'已接收字节数','data':bytes_recv_list},{'name':'已发送包数','data':packets_sent_list},{'name':'已接收包数','data':packets_recv_list}]
    return data

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
    cpus = models.Cpu.objects.filter(server=server)
    data = {}
    cpu_data = []
    for cpu in cpus:
        cpu_data.append([get_time_stamp13(cpu.create_time),float(cpu.percent_avg)])
    mem_data = []
    mems = models.Mem.objects.filter(server=server)
    for mem in mems:
        mem_data.append([get_time_stamp13(mem.create_time),float(mem.percent)])

    swap_data = []
    swaps = models.Swap.objects.filter(server=server)
    for swap in swaps:
        swap_data.append([get_time_stamp13(swap.create_time), float(swap.percent)])

    data['cpu_percent_avg'] = cpu_data
    data['mem_percent_avg'] = mem_data
    data['swap_percent_avg'] = swap_data

    disks = models.Disk.objects.filter(server=server)
    diskdata = []
    row = 0
    col = 0
    row_num = 100
    col_num = 100
    interval_num = 300
    for disk in disks:
        diskdetail = models.DiskDetail.objects.filter(disk=disk).order_by('-create_time').first()
        detail_list = []
        detail_list.append(['已使用', float('%.2f' % float(diskdetail.percent))])
        detail_list.append(['空闲', float('%.2f' % (100 - float(diskdetail.percent)))])
        center = [col_num+(interval_num*col),row_num+(interval_num*row)]
        diskdata.append({'mountpoint':str(disk.mountpoint.replace('\\','/')),'center':center, 'detail_list':detail_list,'disk':diskdetail})
        if col == 2:
            col = 0
            row += 1
        else:
            col += 1

    context['server'] = server
    context['nets'] = nets
    context['type'] = type
    context['targets'] = data
    context['diskdatas'] = diskdata
    context['netdatas'] = GetNet(server)
    return render(request,'serverDetail.html',context)

def GetCpu(request,server_pk):
    cpus = models.Cpu.objects.filter(server_id=server_pk)
    cpu_data = []
    for cpu in cpus:
        cpu_data.append([get_time_stamp13(cpu.create_time), float(cpu.percent_avg)])
    data = {}
    data['status'] = 'SUCCESS'
    data['data'] = cpu_data
    return JsonResponse(data)

import time
def DateTimeToTimestamp(dt):
    timestamp = int(time.mktime(dt.timetuple()))
    return timestamp

def get_time_stamp13(datetime_obj):

    # 生成13时间戳   eg:1557842280000
    datetime_str = datetime.datetime.strftime(datetime_obj, '%Y-%m-%d %H:%M:%S')
    datetime_obj = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    # 10位，时间点相当于从1.1开始的当年时间编号
    date_stamp = str(int(time.mktime(datetime_obj.timetuple())))
    # 3位，微秒
    data_microsecond = str("%06d" % datetime_obj.microsecond)[0:3]
    date_stamp = date_stamp + data_microsecond
    return int(date_stamp)

def stampToTime(stamp):
    datatime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(str(stamp)[0:10])))
    datatime = datatime+'.'+str(stamp)[10:]
    return datatime

'''
def GetCpuInfo(request,server_pk):
    cpus = models.Cpu.objects.filter(server_id=server_pk)
    data = []
    cpudata = []
    for cpu in cpus:
        cpu_time = get_time_stamp13(cpu.create_time)
        print(cpu_time)
        cpudata.append([get_time_stamp13(cpu.create_time), float(cpu.percent_avg)])
        print(stampToTime(cpu_time))
    data.append(cpudata)
    return HttpResponse(data,content_type="application/json,charset=utf-8")
'''

def GetMem(request,server_pk):
    mems = models.Mem.objects.filter(server_id=server_pk)
    mem_data = []

    for mem in mems:
        mem_data.append([get_time_stamp13(mem.create_time), float(mem.percent)])
    data = {}
    data['status'] = 'SUCCESS'
    data['data'] = mem_data
    return JsonResponse(data)

def GetSwap(request,server_pk):
    swap_data = []
    swaps = models.Swap.objects.filter(server_id=server_pk)
    for swap in swaps:
        swap_data.append([get_time_stamp13(swap.create_time), float(swap.percent)])
    data = {}
    data['status'] = 'SUCCESS'
    data['data'] = swap_data
    return JsonResponse(data)

def GetNetInfo(request,server_pk):
    server = models.Server.objects.get(pk=server_pk)
    data = {}
    data['status'] = 'SUCCESS'
    data['datas'] = GetNet(server)['datas']
    return JsonResponse(data)




