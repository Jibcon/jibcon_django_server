from django.contrib import admin
from .models import Device, UserInfo, House, Routine

# Register your models here.
admin.site.register(Device)
admin.site.register(UserInfo)
admin.site.register(House)
admin.site.register(Routine)