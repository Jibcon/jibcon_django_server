from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.


# todo specify class fields
from rest_framework.authtoken.models import Token


class UserInfo(models.Model):
     user = models.OneToOneField(settings.AUTH_USER_MODEL)
     full_name = models.CharField(max_length=20, default='')
     age_range = models.CharField(max_length=20, default='')
     gender = models.CharField(default='', max_length=10)
     pic_url = models.URLField(default='')
     locale = models.CharField(max_length=10, default='')
     # def

variableHouseTypes = [
    "아파트",
    "사무실",
    "자취방",
    "저택",
    "모스크",
]

class House(models.Model):
    adminUser = models.ForeignKey(User, on_delete=models.CASCADE) # todo on_delete -> when all of groupmember deleted
    houseType = models.CharField(max_length=255, default=variableHouseTypes[2])
    houseName = models.CharField(max_length=255, default="찬주의 자취방")
    houseIntro = models.CharField(max_length=255, default="고양이가 있는 짠주의 자취방이에욥")
    houseLocation = models.CharField(max_length=255, default="서울시 성북구 안암동 1, 고려대학교 파이빌 91호")

variableDeviceTypes = [
    "에어컨",
    "선풍기",
    "전구",
    "플러그",
]

class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deviceCom = models.CharField(max_length=255,default="찬주 일렉트로닉스")
    deviceName = models.CharField(max_length=255,default="동그라미플러그")
    deviceWifiAddr = models.CharField(max_length=255,default="127.0.0.0")
    deviceType = models.CharField(max_length=255,default=variableDeviceTypes[0])
    deviceOnOffState = models.BooleanField(default=False)