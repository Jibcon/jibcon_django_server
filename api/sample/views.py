from random import randint


from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.serializers import UserSerializer


@api_view(['GET'])
def GetSampleUser(request):
    serializer_class = UserSerializer

    def plus_token_to_data(data):
        user = User.objects.filter(username=data['username']).first()
        token, created = Token.objects.get_or_create(user=user)
        print("token : " + token.key)

        data['token'] = token.key
        return data

    samples = ["sample_01",
                "sample_02",
                "sample_03",
                "sample_04",
                "sample_05",
               ]

    samplenum = randint(0, 4)

    print("Rnd : {}, SampleName : {}".format(randint,samples[samplenum]))

    user = User.objects.get(
        username=samples[samplenum],
    )

    serializer = serializer_class(user)

    response = plus_token_to_data(serializer.data)
    return Response(data=response, status=status.HTTP_200_OK)