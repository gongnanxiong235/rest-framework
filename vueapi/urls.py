from django.urls import path, re_path
from vueapi import views as v

urlpatterns = [
    # re_path(r'^(?P<version>v[0-9].[0-9]+)/bloglist/$', v.BlogList.as_view({'get':'list'})),
    path('bloglist', v.BlogList.as_view({'get': 'list'})),
    path('blogadd', v.BlogCreate.as_view()),
    path('blogupdate', v.BlogUpdate.as_view()),
    path('blogdelete', v.BlogDelete.as_view()),
    path('blogseach', v.BlogSeach.as_view()),

]
