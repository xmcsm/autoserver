from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from respository import models
import json


# 分析服务器基本信息
def hardwarehandle(res,server_obj):
    status = res['Hardware']['status']
    if status != 10000:
        models.ErrorLog.objects.create(content=res['Hardware']['data']['message'], server=server_obj,
                                       title='服务器同步失败')
        return

    if 'basic' in res['Hardware']['data'].keys():
        server_obj.os_platform = res['Hardware']['data']['basic']['os_platform']
        server_obj.os_version = res['Hardware']['data']['basic']['os_version']
        server_obj.hostname = res['Hardware']['data']['basic']['hostname']
    if 'board' in res['Hardware']['data'].keys():
        server_obj.manufacturer = res['Hardware']['data']['board']['Manufacturer']
        server_obj.model = res['Hardware']['data']['board']['Product Name']
        server_obj.sn = res['Hardware']['data']['board']['Serial Number']
    if 'cpu' in res['Hardware']['data'].keys():
        server_obj.cpu_count = res['Hardware']['data']['cpu']['cpu_count']
        server_obj.cpu_physical_count = res['Hardware']['data']['cpu']['cpu_physical_count']
        server_obj.cpu_model = res['Hardware']['data']['cpu']['cpu_model']
        print(res['Hardware']['data']['cpu']['cpu_physical_count'])
        print(server_obj.cpu_physical_count)
    if 'mem' in res['Hardware']['data'].keys():
        server_obj.mem_total = res['Hardware']['data']['mem']

    server_obj.is_sync = True
    server_obj.save()

# 分析CPU数据
def cpuhandle(res,server_obj):
    status = res['Cpu']['status']
    if status != 10000:
        models.ErrorLog.objects.create(content=res['Cpu']['data']['message'], server=server_obj, title='CPU同步失败')

    cpu = models.Cpu()
    cpu.server = server_obj
    cpu.percent_avg = res['Cpu']['data']['percent_avg']
    cpu.percent_per = res['Cpu']['data']['percent_per']
    cpu.save()

# 分析内存数据
def memhandle(res,server_obj):
    status = res['Mem']['status']
    if status != 10000:
        models.ErrorLog.objects.create(content=res['Mem']['data']['message'], server=server_obj, title='内存同步失败')

    mem = models.Mem()
    mem.server = server_obj
    mem.mem_total = res['Mem']['data']['total']
    mem.used = res['Mem']['data']['used']
    mem.free = res['Mem']['data']['free']
    mem.percent = res['Mem']['data']['percent']
    mem.save()

# 分析交换分区数据
def swaphandle(res,server_obj):
    status = res['Swap']['status']
    if status != 10000:
        models.ErrorLog.objects.create(content=res['Swap']['data']['message'], server=server_obj, title='交换分区同步失败')

    swap = models.Swap()
    swap.server = server_obj
    swap.total = res['Swap']['data']['total']
    swap.used = res['Swap']['data']['used']
    swap.free = res['Swap']['data']['free']
    swap.percent = res['Swap']['data']['percent']
    swap.save()

# 分析磁盘数据
def diskhandle(res,server_obj):
    status = res['Disk']['status']
    if status != 10000:
        models.ErrorLog.objects.create(content=res['Disk']['data']['message'], server=server_obj, title='磁盘同步失败')

    new_disk_info = res['Disk']['data']
    new_disk = list(new_disk_info.keys())

    old_disk_info = models.Disk.objects.filter(server=server_obj)
    old_disk = []
    for obj in old_disk_info:
        old_disk.append(obj.device)

    #新增磁盘
    add_slot = set(new_disk).difference(set(old_disk))
    if add_slot:
        record_list = []
        for slot in add_slot:
            disk_res = new_disk_info[slot]
            disk_res['total'] = disk_res['used']['total']
            tmp = '[新增磁盘{device},挂载点{mountpoint},磁盘类型{fstype},容量{total}G]'.format(**disk_res)
            disk = add_disk(server_obj, disk_res)
            add_disk_detail(disk, disk_res['used'])
            record_list.append(tmp)
        models.ChangeLog.objects.create(content=';'.join(record_list), server=server_obj)

    # 删除磁盘
    del_slot = set(old_disk).difference(set(new_disk))
    if del_slot:
        record_list = []
        for slot in del_slot:
            delete_disk = models.Disk.objects.filter(device=slot, server=server_obj).first()
            models.DiskDetail.objects.filter(disk=delete_disk).delete()
            delete_disk.delete()
            tmp = '删除磁盘{0}'.format(slot)
            record_list.append(tmp)
        models.ChangeLog.objects.create(content=';'.join(record_list), server=server_obj)

    up_slot = set(new_disk).intersection(set(old_disk))
    if up_slot:
        record_list = []
        for slot in up_slot:
            new_disk_row = new_disk_info[slot]
            new_disk_row['total'] = new_disk_row['used']['total']
            old_disk_row = models.Disk.objects.filter(device=slot,server=server_obj).first()
            add_disk_detail(old_disk_row, new_disk_row['used'])
            for k,new_v in new_disk_row.items():
                if k == 'used':
                    continue
                old_v = getattr(old_disk_row,k)

                if str(new_v) != old_v:
                    tmp = '[磁盘{0}变更,{1}由{2}变成{3}]'.format(slot,k,old_v,new_v)
                    record_list.append(tmp)
                    setattr(old_disk_row,k,new_v)

            old_disk_row.save()
        if record_list:
            models.ChangeLog.objects.create(content=';'.join(record_list), server=server_obj)

# 新增磁盘
def add_disk(server_obj,disk_res):
    disk = models.Disk()
    disk.server = server_obj
    disk.device = disk_res['device']
    disk.mountpoint = disk_res['mountpoint']
    disk.fstype = disk_res['fstype']
    disk.opts = disk_res['opts']
    disk.total = disk_res['total']
    disk.save()
    return disk

# 添加磁盘使用信息
def add_disk_detail(disk,devused):
    diskdetail = models.DiskDetail()
    diskdetail.disk = disk
    diskdetail.total = devused['total']
    diskdetail.used = devused['used']
    diskdetail.free = devused['free']
    diskdetail.percent = devused['percent']
    diskdetail.save()

# 分析网卡数据
def nethandle(res,server_obj):
    status = res['Net']['status']
    if status != 10000:
        models.ErrorLog.objects.create(content=res['Net']['data']['message'], server=server_obj,
                                       title='网卡同步失败')

    new_net_info = res['Net']['data']
    if '127.0.0.1' in new_net_info.keys():
        del new_net_info['127.0.0.1']
    new_net = list(new_net_info.keys())
    old_net_info = models.Net.objects.filter(server=server_obj)
    old_net = []
    for obj in old_net_info:
        old_net.append(obj.address)

    #新增网卡
    add_nic = set(new_net).difference(set(old_net))
    if add_nic:
        record_list = []
        for nic in add_nic:
            net_res = new_net_info[nic]
            tmp = '[新增网卡{name},类型{family},IP{address},子关掩码{netmask}]'.format(**net_res)
            add_net(server_obj, net_res)
            record_list.append(tmp)
        models.ChangeLog.objects.create(content=';'.join(record_list), server=server_obj)

    # 删除网卡
    del_nic = set(old_net).difference(set(new_net))
    if del_nic:
        record_list = []
        for nic in del_nic:
            delete_net = models.Net.objects.filter(address=nic, server=server_obj).first().delete()
            tmp = '删除网卡{0}'.format(nic)
            record_list.append(tmp)
        models.ChangeLog.objects.create(content=';'.join(record_list), server=server_obj)

    up_nic = set(new_net).intersection(set(old_net))
    if up_nic:
        record_list = []
        for nic in up_nic:
            new_net_row = new_net_info[nic]
            old_net_row = models.Net.objects.filter(address=nic,server=server_obj).first()
            for k,new_v in new_net_row.items():
                if getattr(old_net_row,k,False):
                    old_v = getattr(old_net_row,k)
                    if str(new_v) != old_v:
                        tmp = '[网卡{0}变更,{1}由{2}变成{3}]'.format(nic,k,old_v,new_v)
                        record_list.append(tmp)
                        setattr(old_net_row,k,new_v)

            old_net_row.save()
        if record_list:
            models.ChangeLog.objects.create(content=';'.join(record_list), server=server_obj)

# 新增网卡
def add_net(server_obj,nic):
    net = models.Net()
    net.server = server_obj
    net.name = nic['name']
    net.family = nic['family']
    net.address = nic['address']
    net.netmask = nic['netmask']
    net.broadcast = nic['broadcast']
    net.bytes_sent = nic['bytes_sent']
    net.bytes_recv = nic['bytes_recv']
    net.packets_sent = nic['packets_sent']
    net.packets_recv = nic['packets_recv']
    net.save()
    return net



@csrf_exempt
def asset(request):
    res = json.loads(request.body)
    ipaddr = res['CLIENTIP']
    server_obj = models.Server.objects.filter(ipaddr=ipaddr).first()
    if not server_obj:
        return HttpResponse('资产未录入！')
    #### 同步服务器信息
    if not server_obj.is_sync:
        if 'Hardware' in res.keys():
            hardwarehandle(res,server_obj)

    #### 分析磁盘数据
    if 'Disk' in res.keys():
        diskhandle(res,server_obj)

    # #### 分析CPU数据
    if 'Cpu' in res.keys():
        cpuhandle(res,server_obj)

    # #### 分析内存数据
    if 'Mem' in res.keys():
        memhandle(res,server_obj)

    # #### 分析交换分区数据
    if 'Swap' in res.keys():
        swaphandle(res, server_obj)
    #
    # #### 分析网卡数据
    if 'Net' in res.keys():
        nethandle(res,server_obj)

    return HttpResponse('ok')