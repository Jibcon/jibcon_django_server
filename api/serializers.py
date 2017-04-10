from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        from django.contrib.auth.models import User
        model = User
        fields = ('email',)

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