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

     def __str__(self):
         return self.full_name

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

DEVICECOM_CHOICES = (
    ("smArts", "smArts"),
    ("smArts", "smArts"),
    ("smArts", "smArts"),
    ("Philips", "Philips"),
    ("Philips", "Philips"),
)

DEVICENAME_CHOICES = (
    ("led", "LED전등"),
    ("ultra", "초음파감지기"),
    ("humidity", "온습도측정"),
    ("Philips Hue 전구", "hue"),
    ("Philips Hue 전구 - 현관", "hue-현관"),
)

DEVICETYPE_CHOICES = (
    ("bulb", "전등"),
    ("ultrasensor", "초음파센서"),
    ("humiditysensor", "온습도센서"),
    ("hue-bulb", "hue전등"),
    ("hue-bulb-현관", "hue전등-현관"),
)

DEVICEAENAME_CHOICES = (
    ("ae-smarts", "ae-smarts"),
    ("ae-smarts", "ae-smarts"),
    ("ae-smarts", "ae-smarts"),
    ("ae-smarts", "ae-smarts"),
    ("ae-smarts", "ae-smarts"),
)

DEVICECNTNAME_CHOICES = (
    ("cnt-led", "cnt-led"), # _req _res 둘다만들기
    ("cnt-ultra", "cnt-ultra"),
    ("cnt-dht", "cnt-dht"),
    ("cnt-hue", "cnt-hue"),
    ("cnt-hue", "cnt-hue"),
)

class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deviceCom = models.CharField(choices=DEVICECOM_CHOICES, max_length=255, default=DEVICECOM_CHOICES[0][0])
    deviceName = models.CharField(choices=DEVICENAME_CHOICES, max_length=255, default=DEVICENAME_CHOICES[0][0])
    deviceType = models.CharField(choices=DEVICETYPE_CHOICES, max_length=255, default=DEVICETYPE_CHOICES[0][0])
    aeName = models.CharField(choices=DEVICEAENAME_CHOICES, max_length=255,default=DEVICEAENAME_CHOICES[0][0])
    cntName = models.CharField(choices=DEVICECNTNAME_CHOICES, max_length=255,default=DEVICECNTNAME_CHOICES[0][0])
    deviceOnOffState = models.BooleanField(default=False)
    subscribeOnOffState = models.BooleanField(default=False)
    roomName = models.CharField(max_length=255,default="거실")

    def __str__(self):
        return self.user.username + " " + self.deviceName


ROUTINE_CONDITIONMETHOD_CHOICES = (
    ("larger", ">"),
    ("smaller", "<"),
    ("equal", "="),
)

class Routine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255,default="현관문에 사람이 지나가면 Phillips Hue 전구를 켜줘.")
    sensor = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_related_sensor')
    conditionMethod = models.CharField(choices=ROUTINE_CONDITIONMETHOD_CHOICES, max_length=255, default=DEVICECOM_CHOICES[0][0])
    value = models.CharField(max_length=255,default="0.1")
    unit = models.CharField(max_length=255,default="m")
    actuator = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_related_actuator')

    def __str__(self):
        return self.user.username + " " + self.title
#
# class DeviceCompany(models.Model):
#     englishName = models.CharField(unique=True, max_length=255, default="smArts")
#     koreanName = models.CharField(unique=True, max_length=255, default="smArts")
#
#     def __str__(self):
#         return self.englishName
#
# class Device