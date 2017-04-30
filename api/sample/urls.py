from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^sign_in/$', views.GetSampleUser, name='get_sample_user'),
]
