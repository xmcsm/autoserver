from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Server)
admin.site.register(models.Disk)
admin.site.register(models.Product)
admin.site.register(models.ChangeLog)
admin.site.register(models.Area)
admin.site.register(models.Cpu)
admin.site.register(models.DiskDetail)
admin.site.register(models.ErrorLog)
admin.site.register(models.Mem)
admin.site.register(models.NetDetail)
admin.site.register(models.Net)
admin.site.register(models.Tag)
admin.site.register(models.UserProfile)