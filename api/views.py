#-*- coding:utf-8 -*-
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.http import HttpResponse
from api.serializers import UserSerializer
from .serializers import DeviceSerializer
from .models import Device, UserInfo
from .permissions import IsOwnerOrSuperUser


# Create your views here
class SocialSignUpOrIn(generics.CreateAPIView):
    """
    페이스북 토큰으로 로그인
    
    가능 메소드 : [ get ]
    
    get : 페이스북 토큰으로 로그인<br>
    예시 : <br>
    {\<br>
        "username\":\"facebook_725109100996336\",\<br>
        "email\":\"pjo901018@naver.com\",\<br>
        "userinfo\":<br>
        {\<br>
            "age_range\":\"min\",\<br>
            "gender\":\"male\",<br>
            \"pic_url\":\"ht",
            "tps://scontent.xx.fbcdn.net/v/t1.0-1/p50x50/14202642_625021034338477_6992400572239206628_n.jpg?oh=bd2188618ba461bdb2a691b3d20165",
            "19&oe=598597CF\"<br>
        },<br>
        \"token\":\"6aeb01e64263f9c4cd85b8c8e1097f8a0868dff9\"<br>
    }"
    """
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

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
            from jibcon_django_server.settings import INTERNAL_DOMAIN
            domain = INTERNAL_DOMAIN
            endpoints = "api/user_sign_up_or_in/"
            import requests
            response = requests.post(domain + endpoints, data=userinfo)
            return Response(response)
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

        return self.post_to_user_sign_up_or_in(userinfo)

class UserInfo(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    # queryset = User.objects.all()

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

class UserSignUpOrIn(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    # def auto_create_pwd(self):
    #     return "1234qwer"

    def get_token(self, data):
        user = User.objects.filter(username=data['username']).first()
        token, created = Token.objects.get_or_create(user=user)
        print("token : "+token.key)
        return token.key

    def perform_create(self, serializer):
        serializer.is_valid()
        user = serializer.save()

        from .models import UserInfo
        UserInfo.objects.create(
                user = user,
                pic_url=self.request.data['pic_url'],
                gender=self.request.data['gender'],
                age_range= self.request.data['age_range']
                                  )

    def post(self, request, *args, **kwargs):
        log = "request data : "
        for each in request.data:
            log = log + each + ','
        print(log)

        try :
            user = User.objects.get(
                username=request.data.get('username'),
            )

            serializer = self.serializer_class(user)

            # return self.perform_create(serializer)
            response = serializer.data
            response['token'] = self.get_token(serializer.data)
            return Response(response, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            pass

        serializer = self.get_serializer(data=request.data)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        response = serializer.data
        response['token'] = self.get_token(serializer.data)
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)

class UserSignedCheck(generics.CreateAPIView):
    from api.serializers import UserSignedSerializer
    serializer_class = UserSignedSerializer
    permission_classes = (AllowAny,)

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
        if not self.is_valid_requestbody():
            return Response({'detail': "Unexpected arguments", 'args': ['username', 'token']},
                            status=status.HTTP_400_BAD_REQUEST)

        # phonenumber or email
        username = request.data['username']
        token = request.data['token']


        serializer = self.serializer_class({ "signed" : self.is_signed(username, token) })
        return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework import mixins
class DeviceList(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                generics.GenericAPIView):

    permission_classes = (IsAuthenticated,IsOwnerOrSuperUser)
    from .models import Device
    queryset = Device.objects.all()

    serializer_class = DeviceSerializer

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
        )

    def is_valid_requestbody(self):
        # todo implement
        return True

    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(user=request.user)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not self.is_valid_requestbody():
            return Response({'detail': "Unexpected arguments", 'args': ['deviceType']},
                            status=status.HTTP_400_BAD_REQUEST)

        return self.create(request, *args, **kwargs)

from rest_framework.generics import RetrieveUpdateDestroyAPIView
class DeviceDetail(RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all().order_by('-uploaded_date')
    serializer_class = DeviceSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrSuperUser)

from .models import House
class HouseList(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                generics.GenericAPIView):

    from .serializers import HouseSerializer
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrSuperUser)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(adminUser=self.request.user)

    def is_valid_requestbody(self):
        # todo implement
        return True

    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(adminUser=request.user)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not self.is_valid_requestbody():
            return Response({'detail': "Unexpected arguments",},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=self.request.data)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class HouseDetail(RetrieveUpdateDestroyAPIView):
    queryset = House.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrSuperUser)