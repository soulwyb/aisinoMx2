# encoding:utf-8
__author__ = 'wuyubin'
__date__ = '2018-09-30 12:31'

from django.urls import re_path, path

from .views import CourseListView, CourseDetialView, CourseInfoView, CommentsView, AddCommentsView

app_name = 'courses'

urlpatterns = [
    path('list/', CourseListView.as_view(), name = 'list'),
    re_path('detail/(?P<course_id>\d+)/', CourseDetialView.as_view(), name = 'course_detail'),
    re_path('info/(?P<course_id>\d+)/', CourseInfoView.as_view(), name = 'course_info'),
    re_path('comments/(?P<course_id>\d+)/', CommentsView.as_view(), name = 'course_comments'),
    re_path('add_comment/', AddCommentsView.as_view(), name = 'add_comment')

]