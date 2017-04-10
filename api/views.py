from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse

from api.serializers import UserSerializer


# Create your views here.
class SocialSignUpOrIn(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    print('SocialSignUpOrIn')

    def is_valid_social(self):
        from social import conf
        if self.request.data['type'] in conf.supply_social_list:
            print('is_valid_social : True')
            return True
        else:
            print('is_valid_social : False')
            return False

    def post(self, request, *args, **kwargs):
        print('SocialSignUpOrIn/post')
        if not self.is_valid_social():
            return Response({'detail' : "Unexpected arguments", 'args' : ['type', 'token']},
                     status = status.HTTP_400_BAD_REQUEST)

        type = request.data['type']
        token = request.data['token']
        if type is 'facebook':
            from social import facebook
            userinfo = facebook.get_userinfo_from_facebook(token)

        # todo createuser
        # todo createuserinfo
        from django.contrib.auth.models import User
        # for test
        user = User.objects.first()

        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserSignedCheck(generics.CreateAPIView):
    from api.serializers import UserSignedSerializer
    serializer_class = UserSignedSerializer
    permission_classes = (AllowAny,)
    print('UserSigninCheck')

    def is_signed(self, username, token):
        # todo implement validation
        if True:
            print('is_signed: True')
            return True
        else:
            print('is_signed: False')
            return False

    def is_valid_requestbody(self):
        # todo implement
        return True

    def post(self, request, *args, **kwargs):
        print('UserSignedCheck/post')
        if not self.is_valid_requestbody():
            return Response({'detail': "Unexpected arguments", 'args': ['email', 'token']},
                            status=status.HTTP_400_BAD_REQUEST)

        # phonenumber or email
        username = request.data['username']
        token = request.data['token']


        serializer = self.serializer_class({ "signed" : self.is_signed(username, token) })
        return Response(serializer.data, status=status.HTTP_200_OK)