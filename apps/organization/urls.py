# encoding:utf-8
__author__ = 'wuyubin'
__date__ = '2018-09-29 13:12'

from organization.views import OrgView, AddUserAskView, OrgCourseView, OrgHomeView, OrgDescView,OrgTeacherView,AddFavView

from django.urls import re_path, path

app_name = 'organization'

urlpatterns = [
    path('list/', OrgView.as_view(), name="org_list"),
    path('add_ask/', AddUserAskView.as_view(), name = 'add_ask'),
    re_path('course/(?P<org_id>\d+)/', OrgCourseView.as_view(), name = 'org_course'),
    re_path('home/(?P<org_id>\d+)/', OrgHomeView.as_view(), name = 'org_home'),
    re_path('desc/(?P<org_id>\d+)/', OrgDescView.as_view(), name = 'org_desc'),
    re_path('teacher/(?P<org_id>\d+)/', OrgTeacherView.as_view(), name = 'org_teacher'),
    path('add_fav/', AddFavView.as_view(), name = 'add_fav')
]