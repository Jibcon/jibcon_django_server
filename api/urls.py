from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^social_sign_up_or_in/', views.SocialSignUpOrIn.as_view(), name='social_sign_up_or_in'),
    url(r'^user_signed_check/', views.UserSignedCheck.as_view(), name='user_signed_check'),
    url(r'^user_sign_up_or_in/', views.UserSignUpOrIn.as_view(), name='user_sign_up_or_in'),
    url(r'^devices/', views.DeviceList.as_view(), name='device_list'),
    # url(r'^devices/(?P<pk>[0-9]+)/$', views.DeviceDetail.as_view(), name='device_detail'),
]
