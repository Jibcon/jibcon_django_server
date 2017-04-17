from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.


# todo specify class fields
class UserInfo(models.Model):
     user = models.OneToOneField(settings.AUTH_USER_MODEL)
     age_range = models.CharField(max_length=20, default='')
     gender = models.CharField(default='', max_length=10)
     pic_url = models.URLField(default='')

# class Houseinfo(models.Model):
#     pass
#
# class Deviceinfo(models.Model):
#     pass

class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deviceType = models.CharField(max_length=255,default="플러그")
    deviceOnOffState = models.BooleanField(default=False)
