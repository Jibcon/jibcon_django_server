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

    def post_to_user_sign_up_or_in(self, userinfo):
        try:
            # domain = "http://0.0.0.0:8000/"
            domain = "http://localhost:8000/"
            endpoints = "api/user_sign_up_or_in/"
            import requests
            response = requests.post(domain + endpoints, data=userinfo)
            return response
        except:
            pass

    def post(self, request, *args, **kwargs):
        print('SocialSignUpOrIn/post')
        if not self.is_valid_social():
            return Response({'detail' : "Unexpected arguments", 'args' : ['type', 'token']},
                     status = status.HTTP_400_BAD_REQUEST)

        type = request.data['type']
        token = request.data['token']
        print(type)
        if type == 'facebook':
            from social import facebook
            userinfo = facebook.get_userinfo_from_facebook(token)

        # todo createuser
        return self.post_to_user_sign_up_or_in(userinfo)



        from django.contrib.auth.models import User
        # for test
        user = User.objects.first()

        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)




class UserSignUpOrIn(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    print('SignUpOrIn')

    def auto_create_pwd(self):
        return "1234qwer"

    def post(self, request, *args, **kwargs):
        print("post")

        log = "request data : "
        for each in request.data:
            log = log + each + ','
        print(log)

        from django.contrib.auth.models import User
        try :
            user = User.objects.get(
                username=request.data.get('username'),
            )
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            pass

        # password = self.auto_create_pwd()

        # request.data['pic_url']
        # request.data['name']
        # request.data['gender']
        # request.data['age_range']



        # todo createuserinfo
        return self.create(request,
                           # data={'password': password},
                           *args, **kwargs)

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