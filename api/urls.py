from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^social_sign_up_or_in/', views.SocialSignUpOrIn.as_view(), name='social_sign_up_or_in'),
]