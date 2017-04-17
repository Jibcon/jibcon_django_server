from rest_framework import generics
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

            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            pass

        # password = self.auto_create_pwd()

        # request.data['pic_url']
        # request.data['name']
        # request.data['gender']
        # request.data['age_range']

        return self.perform_create(serializer)

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