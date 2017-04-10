from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

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