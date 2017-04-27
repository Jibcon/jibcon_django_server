#-*- coding:utf-8 -*-
from drf_autodocs.decorators import format_docstring
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

from api.docs.request_response_examples import *
from api.serializers import UserSerializer, UserSignedSerializer, SocialTokenSerializer
from .serializers import DeviceSerializer
from .models import Device, UserInfo
from .permissions import IsOwnerOrSuperUser


# Create your views here
@format_docstring(post_SocialSignUpOrIn_request, response_example=post_SocialSignUpOrIn_response)
class SocialSignUpOrIn(generics.CreateAPIView):
    """
    페이스북 토큰으로 로그인
    
    가능 메소드 : [ POST ]
    
    Request: {}
    Response: {response_example}
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
            if 'error' in userinfo:
                return Response(userinfo['error'],
                         status=status.HTTP_400_BAD_REQUEST)

        response = self.post_to_user_sign_up_or_in(userinfo)

        if response.ok:
            return Response(response.json(), status=response.status_code)
        else:
            return response

@format_docstring(get_user_info_request, response_example=post_SocialSignUpOrIn_response)
class UserInfo(generics.ListAPIView):
    """
    User 정보
    
    가능 메소드 : [ GET ]
    
    Request: {}
    Response: {response_example}
    """

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    # queryset = User.objects.all()

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

class UserSignUpOrIn(generics.CreateAPIView):
    """
    서버 내부 호출용
    """
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    # def auto_create_pwd(self):
    #     return "1234qwer"

    def plus_token_to_data(self, data):
        user = User.objects.filter(username=data['username']).first()
        token, created = Token.objects.get_or_create(user=user)
        print("token : "+token.key)

        data['token'] = token.key
        return data

    def perform_create(self, serializer):

        def get_full_name(first,last):
            # if locale todo
            return last+first

        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        from .models import UserInfo
        UserInfo.objects.create(
                user = user,
                pic_url=self.request.data['pic_url'],
                gender=self.request.data['gender'],
                age_range= self.request.data['age_range'],
                locale = self.request.data['locale'],
                full_name = self.request.data['name']
                                  )
        return serializer

    def post(self, request, *args, **kwargs):
        log = "request data : "
        for each in request.data:
            log = log + each + ','
        print(log)


        data = request.data.dict()

        try :
            user = User.objects.get(
                username=data.get('username'),
            )

            serializer = self.serializer_class(user)

            response = self.plus_token_to_data(serializer.data)
            return Response(data=response, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            serializer = self.get_serializer(data=data)
            serializer = self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            response = self.plus_token_to_data(serializer.data)
            return Response(data=response, status=status.HTTP_201_CREATED, headers=headers)


@format_docstring(get_user_signed_check_request, response_example=get_user_signed_check_response)
class UserSignedCheck(generics.CreateAPIView):
    """
    User 로그인여부 확인(토큰만료검사)

    가능 메소드 : [ GET ]

    Request: {}
    Response: {response_example}
    """
    serializer_class = UserSignedSerializer
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        # phonenumber or email
        serializer = self.serializer_class({ "signed" : self.request.user.is_authenticated })
        return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework import mixins
@format_docstring(get_user_info_request, response_example=get_devices_response,
                  post_request_example=post_devices_request,
                  post_response_example=post_devices_response)
class DeviceList(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                generics.GenericAPIView):
    """
    Device List
    
    가능 메소드 : [ GET, Post ]

    [ GET ]
    Request: {}
    Response: {response_example}
    
    [ POST ]
    Request: {post_request_example}
    Response: {post_response_example}
    """

    permission_classes = (IsAuthenticated,IsOwnerOrSuperUser)
    from .models import Device
    queryset = Device.objects.all()

    serializer_class = DeviceSerializer

    def perform_create(self, serializer):

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer

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

        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.serializer_class(data=data)
        serializer = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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