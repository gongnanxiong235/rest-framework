from django.urls import path,re_path
from restapi import views as v

urlpatterns = [
    re_path(r'^(?P<version>v[0-9].[0-9]+)/auth/$', v.AuthView.as_view()),
    re_path(r'^(?P<version>v[0-9].[0-9]+)/regist/$', v.RegistView.as_view()),
    # path('api/vi/order', v.OrderView.as_view()),
    # path('api/vi/userinfo', v.UserInfo.as_view()),
    re_path(r'^(?P<version>v[0-9].[0-9]+)/order/$', v.OrderView.as_view()),
    re_path(r'^(?P<version>v[0-9].[0-9]+)/userinfo/$', v.UserInfo.as_view()),
    re_path(r'^(?P<version>v[0-9].[0-9]+)/version/$', v.Version.as_view(),name='user'),
    re_path(r'^(?P<version>v[0-9].[0-9]+)/parse/$', v.ParseView.as_view()),
    re_path(r'^(?P<version>v[0-9].[0-9]+)/role/$', v.Roleview.as_view()),
    re_path(r'^(?P<version>v[0-9].[0-9]+)/userdetail/$', v.UseretailView.as_view()),
    re_path(r'^(?P<version>v[0-9].[0-9]+)/userdetail3/$', v.UserDetailLink.as_view()),
    re_path(r'^(?P<version>v[0-9].[0-9]+)/group/(?P<pk>\d+)/$', v.GroupView.as_view(),name='gp'),
    re_path(r'^(?P<version>v[0-9].[0-9]+)/page1/$', v.PageView.as_view()),
    re_path(r'^(?P<version>v[0-9].[0-9]+)/page2/$', v.LimitPageView.as_view()),
    re_path(r'^(?P<version>v[0-9].[0-9]+)/page3/$', v.CursorPageView.as_view()),
    re_path(r'^(?P<version>v[0-9].[0-9]+)/gen/$', v.GenericView.as_view()),
    re_path(r'^(?P<version>v[0-9].[0-9]+)/model/$', v.ViewsetView.as_view({'get':'list'})),
    re_path(r'^(?P<version>v[0-9].[0-9]+)/model2/$', v.ViewsetView1.as_view({'get':'list'})),
    re_path(r'^(?P<version>v[0-9].[0-9]+)/model2/(?P<pk>\d+)$', v.ViewsetView1.as_view({'get':'retrieve'})),
]
