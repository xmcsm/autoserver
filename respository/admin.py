from django.contrib import admin

# Register your models here.
from . import models

@admin.register(models.Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ('id','device_type_id','device_status_id','ipaddr','hostname','os_platform','os_version','manufacturer','model','sn')

@admin.register(models.Cpu)
class CpuAdmin(admin.ModelAdmin):
    list_display = ('id','server','percent_avg','percent_per','create_time')

@admin.register(models.Mem)
class MemAdmin(admin.ModelAdmin):
    list_display = ('id','server','mem_total','used','free','percent','create_time')

@admin.register(models.Disk)
class DiskAdmin(admin.ModelAdmin):
    list_display = ('id','server','device','mountpoint','fstype','opts','total')

@admin.register(models.DiskDetail)
class DiskDetailAdmin(admin.ModelAdmin):
    list_display = ('id','disk','total','used','free','percent','create_time')

@admin.register(models.Net)
class NetAdmin(admin.ModelAdmin):
    list_display = ('id','server','name','family','address','netmask','broadcast')

@admin.register(models.NetDetail)
class NetDetailAdmin(admin.ModelAdmin):
    list_display = ('id','net','bytes_sent','bytes_recv','packets_sent','packets_recv','create_time')

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name')

@admin.register(models.Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('id','name')

admin.site.register(models.ChangeLog)
admin.site.register(models.ErrorLog)

admin.site.register(models.Tag)
admin.site.register(models.UserProfile)