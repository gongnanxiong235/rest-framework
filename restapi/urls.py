from django.urls import path,re_path
from restapi import views as v

urlpatterns = [
    re_path(r'^(?P<version>v[0-9].[0-9]+)/auth/$', v.AuthView.as_view()),
    # path('api/vi/order', v.OrderView.as_view()),
    # path('api/vi/userinfo', v.UserInfo.as_view()),
    re_path(r'^(?P<version>v[0-9].[0-9]+)/order/$', v.OrderView.as_view()),
    re_path(r'^(?P<version>v[0-9].[0-9]+)/userinfo/$', v.UserInfo.as_view()),
    re_path(r'^(?P<version>v[0-9].[0-9]+)/version/$', v.Version.as_view(),name='user'),
]
