from django.db import models
from datetime import datetime

# Create your models here.
class UserProfile(models.Model):
    username = models.CharField(u'姓名',max_length=32)
    password = models.CharField(u'密码',max_length=64)
    phone = models.CharField(u'手机',max_length=32)
    email = models.EmailField(u'姓名')

    class Meta:
        verbose_name_plural = '用户表'

    def __str__(self):
        return self.username


class Product(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = '业务系统'

    def __str__(self):
        return self.name

class Area(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = '地区表'

    def __str__(self):
        return self.name

class Server(models.Model):

    device_type_choices = (
        (1, '服务器'),
        (2, '交换机'),
        (3, '防火墙'),
    )

    device_status_choices = (
        (1, '在运'),
        (2, '退运'),
    )
    device_sync_choices = (
        (0, '未同步'),
        (1, '已同步'),
    )
    device_type_id = models.IntegerField('服务器类型',choices=device_type_choices,default=1)
    device_status_id = models.IntegerField('服务器状态', choices=device_status_choices, default=1)

    ipaddr = models.CharField('IP',max_length=128,unique=True)
    hostname = models.CharField('主机名',max_length=128,null=True,blank=True)
    os_platform = models.CharField('操作系统',max_length=32,null=True,blank=True)
    os_version = models.CharField('操作系统版本',max_length=128,null=True,blank=True)
    manufacturer = models.CharField('制造商',max_length=128,null=True,blank=True)
    model = models.CharField('主板型号',max_length=128,null=True,blank=True)
    sn = models.CharField('SN号',max_length=128,null=True,blank=True,db_index=True)

    area = models.ForeignKey('Area',verbose_name='地区',null=True,blank=True,on_delete=models.CASCADE)
    idc = models.CharField('机房',max_length=128,null=True,blank=True)
    cabinet = models.CharField('机柜位置',max_length=128,null=True,blank=True)

    cpu_count = models.IntegerField('CPU个数',null=True,blank=True)
    cpu_physical_count = models.IntegerField('CPU物理个数',null=True,blank=True)
    cpu_model = models.CharField('CPU型号',max_length=128,null=True,blank=True)
    mem_total = models.CharField('内存总量',max_length=50,null=True,blank=True)
    product = models.ForeignKey('Product',verbose_name='业务系统',on_delete=models.CASCADE)

    create_time = models.DateTimeField(auto_now_add=True,blank=True)

    tag = models.ManyToManyField('Tag',null=True,blank=True)

    is_sync = models.IntegerField('同步状态', choices=device_sync_choices, default=0)
    class Meta:
        verbose_name_plural = '服务器表'

    def __str__(self):
        return self.ipaddr


class Cpu(models.Model):
    server = models.ForeignKey('Server',related_name='cpu',on_delete=models.CASCADE)
    percent_avg = models.CharField('平均使用率',max_length=50)
    percent_per = models.CharField('每个CPU使用率',max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'CPU信息表'

    def __str__(self):
        return self.percent_avg


class Mem(models.Model):
    server = models.ForeignKey('Server',related_name='mem' ,on_delete=models.CASCADE)
    mem_total = models.CharField('总内存',max_length=50,null=True,blank=True)
    used = models.CharField('已使用内存',max_length=50,null=True,blank=True)
    free = models.CharField('空闲内存',max_length=50,null=True,blank=True)
    percent = models.CharField('使用率',max_length=50,null=True,blank=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '内存信息表'

    def __str__(self):
        return self.mem_total

class Swap(models.Model):
    server = models.ForeignKey('Server',related_name='swap',verbose_name='服务器' ,on_delete=models.CASCADE)
    total = models.CharField('总Swap',max_length=50,null=True,blank=True)
    used = models.CharField('已使用Swap',max_length=50,null=True,blank=True)
    free = models.CharField('空闲Swap',max_length=50,null=True,blank=True)
    percent = models.CharField('使用率',max_length=50,null=True,blank=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '交换分区表'

    def __str__(self):
        return self.total


class Disk(models.Model):
    server = models.ForeignKey('Server', related_name='disk',on_delete=models.CASCADE)
    device = models.CharField('盘符',max_length=50)
    mountpoint = models.CharField('挂载点',max_length=50,null=True,blank=True)
    fstype = models.CharField('磁盘类型',max_length=50,null=True,blank=True)
    opts = models.CharField('磁盘权限',max_length=50,null=True,blank=True)
    total = models.CharField('容量',max_length=50,null=True,blank=True)

    class Meta:
        verbose_name_plural = '磁盘表'

    def __str__(self):
        return '%s-%s' % (self.server.ipaddr,self.device)

class DiskDetail(models.Model):
    disk = models.ForeignKey('Disk', on_delete=models.CASCADE)
    total = models.CharField('总容量',max_length=50,null=True,blank=True)
    used = models.CharField('已使用容量',max_length=50,null=True,blank=True)
    free = models.CharField('空闲容量',max_length=50,null=True,blank=True)
    percent = models.CharField('使用率',max_length=50,null=True,blank=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '磁盘信息表'

    def __str__(self):
        return '%s-%s' % (self.disk.server.ipaddr,self.disk.device)

class Net(models.Model):
    server = models.ForeignKey('Server',related_name='net',on_delete=models.CASCADE)
    name = models.CharField('网卡名称',max_length=50,null=True,blank=True)
    family = models.CharField('类型',max_length=50,null=True,blank=True)
    address = models.CharField('IP',max_length=50,null=True,blank=True)
    netmask = models.CharField('子关掩码',max_length=50,null=True,blank=True)
    broadcast = models.CharField('广播地址',max_length=50,null=True,blank=True)
    bytes_sent = models.CharField('已发送字节',max_length=50,default=0)
    bytes_recv = models.CharField('已接收字节',max_length=50,default=0)
    packets_sent = models.CharField('已发送包',max_length=50,default=0)
    packets_recv = models.CharField('已接收包',max_length=50,default=0)

    class Meta:
        verbose_name_plural = '网卡表'

    def __str__(self):
        return self.name

class ErrorLog(models.Model):
    title = models.CharField(max_length=32)
    content = models.TextField()
    server = models.ForeignKey('Server',related_name='el',null=True,blank=True, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '错误日志表'

    def __str__(self):
        return self.title



class ChangeLog(models.Model):
    content = models.TextField(null=True)
    server = models.ForeignKey('Server', related_name='cl',verbose_name='服务器',on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = '资产变更表'

    def __str__(self):
        return '%s-%s' % (self.server.ipaddr,self.server.hostname)


class Tag(models.Model):
    name = models.CharField('标签',max_length=32,unique=True)

    class Meta:
        verbose_name_plural = '标签表'

    def __str__(self):
        return self.name