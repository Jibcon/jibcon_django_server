from rest_framework import serializers


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        from rest_framework.authtoken.models import Token
        model = Token
        fields = (
                'key',
                )

class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField('get_or_create_token')

    class Meta:
        from django.contrib.auth.models import User
        model = User
        fields = (
            'username',
            'email',
            'token',
            # todo unicode
        # utf-8 = unicode(euckr, 'euc-kr').encode('utf-8')

            # 'first_name',
            # 'last_name',
                  )

    def get_or_create_token(self, obj):
        from rest_framework.authtoken.models import Token
        token = Token.objects.get_or_create(user=self.instance)
        print(token)

        serializer = TokenSerializer(token[0])

        return serializer.data



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