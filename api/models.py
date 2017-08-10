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

DEVICENAME_CHOICES = (
    ("led", "LED전등"),
    ("ultra", "초음파감지기"),
    ("humidity", "온습도측정"),
)

DEVICECOM_CHOICES = (
    ("smArts", "smArts"),
)

DEVICETYPE_CHOICES = (
    ("bulb", "전등"),
    ("ultrasensor", "초음파센서"),
    ("humiditysensor", "온습도센서"),
)

DEVICEAENAME_CHOICES = (
    ("ae-smarts", "ae-smarts"),
    ("ae-smarts", "ae-smarts"),
    ("ae-smarts", "ae-smarts"),
)

DEVICECNTNAME_CHOICES = (
    ("cnt-led", "cnt-led"), # _req _res 둘다만들기
    ("cnt-ultra", "cnt-ultra"),
    ("cnt-dht", "cnt-dht"),
)

class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deviceCom = models.CharField(choices=DEVICECOM_CHOICES, max_length=255, default=DEVICECOM_CHOICES[0][0])
    deviceName = models.CharField(choices=DEVICENAME_CHOICES, max_length=255, default=DEVICENAME_CHOICES[0][0])
    deviceType = models.CharField(choices=DEVICETYPE_CHOICES, max_length=255, default=DEVICETYPE_CHOICES[0][0])
    deviceOnOffState = models.BooleanField(default=False)
    subscribeOnOffState = models.BooleanField(default=False)
    roomName = models.CharField(max_length=255,default="거실")
    aeName = models.CharField(choices=DEVICEAENAME_CHOICES, max_length=255,default=DEVICEAENAME_CHOICES[0][0])
    cntName = models.CharField(choices=DEVICECNTNAME_CHOICES, max_length=255,default=DEVICECNTNAME_CHOICES[0][0])

    def __str__(self):
        return self.user.username + " " + self.deviceName