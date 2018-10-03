# encoding:utf-8
__author__ = 'wuyubin'
__date__ = '2018-09-29 13:12'
from django.urls import re_path, path

from .views import UserInfoView, UploadImageView, UpdateEmailView, MyCourseView, MyFavOrgView, MyFavTeacherView,\
    MyFavCourseView, MyMessageView, LogoutView
app_name = 'users'

urlpatterns = [
    path('info/', UserInfoView.as_view(), name = 'user_info'),
    path('image/upload/', UploadImageView.as_view(), name = 'image_upload'),
    path('update_email/', UpdateEmailView.as_view(), name = 'update_email'),
    path('mycourse/', MyCourseView.as_view(), name = 'mycourse'),
    path('myfav/org/', MyFavOrgView.as_view(), name = 'myfav_org'),
    path('myfav/teacher/', MyFavTeacherView.as_view(), name = 'myfav_teacher'),
    path('myfav/course/', MyFavCourseView.as_view(), name = 'myfav_course'),
    path('my_message/', MyMessageView.as_view(), name = 'my_message'),
    path('logout/', LogoutView.as_view(), name = 'logout')

]