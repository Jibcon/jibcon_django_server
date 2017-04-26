from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import UserInfo


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = (
                'key',
                )
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = (
            'age_range',
            'gender',
            'pic_url',
        )

class UserSerializer(serializers.ModelSerializer):
    userinfo = UserInfoSerializer(read_only=True)

    class Meta:
        from django.contrib.auth.models import User
        model = User
        fields = (
            'username',
            'email',
            'userinfo',
            # todo unicode
        # utf-8 = unicode(euckr, 'euc-kr').encode('utf-8')

            # 'first_name',
            # 'last_name',
                  )

class UserSignedSerializer(serializers.Serializer):
    signed = serializers.BooleanField(required=True)

# class UserinfoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Userinfo
#         fields = ()

# For web login(not android)
# class SignUpOrInSerializer(serializers.Serializer):
#     type = serializers.CharField(required=True, allow_blank=False, max_length=255)
#     token = serializers.CharField(required=True, allow_blank=False, max_length=255)

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import Device
        model = Device
        fields = (
            'id',
            'deviceCom',
            'deviceName',
            'deviceType',
            'deviceOnOffState',
            'user_id',
        )

class HouseSerializer(serializers.ModelSerializer):
    adminUserName = serializers.SerializerMethodField('get_adminuser_name')

    class Meta:
        from .models import House
        model = House
        fields = (
        'id',
        'houseType',
        'houseName',
        'houseIntro',
        'houseLocation',
        'adminUser',
        'adminUserName',
        )

    def get_adminuser_name(self, obj):
        if (obj.adminUser):
            return obj.adminUser.get_full_name()
        else:
            return ""