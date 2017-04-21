from django.contrib import admin
from .models import Device,UserInfo,House


# Register your models here.
admin.site.register(Device)
admin.site.register(UserInfo)
admin.site.register(House)