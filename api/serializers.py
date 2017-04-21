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
    token = serializers.SerializerMethodField('get_or_create_token')
    userInfo = serializers.SerializerMethodField('get_user_info')

    class Meta:
        from django.contrib.auth.models import User
        model = User
        fields = (
            'username',
            'email',
            'token',
            'userInfo'
            # todo unicode
        # utf-8 = unicode(euckr, 'euc-kr').encode('utf-8')

            # 'first_name',
            # 'last_name',
                  )

    def get_or_create_token(self, obj):
        from rest_framework.authtoken.models import Token
        token, created = Token.objects.get_or_create(user=obj)

        return token.key

        # serializer = TokenSerializer(token)

        # return serializer.data

    def get_user_info(self, obj):
        userInfo, was_created = UserInfo.objects.get_or_create(user=obj)

        return UserInfoSerializer(userInfo).data

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