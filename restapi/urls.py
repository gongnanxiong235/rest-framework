from django.urls import path
from restapi import views as v

urlpatterns = [
    path('api/vi/auth', v.AuthView.as_view()),
    path('api/vi/order', v.OrderView.as_view()),
    path('api/vi/userinfo', v.UserInfo.as_view()),
]
