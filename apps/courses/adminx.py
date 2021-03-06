# encoding:utf-8
__author__ = 'wuyubin'
__date__ = '2018-09-25 13:53'
import xadmin

from .models import Course, Lesson, Video, CourseResource

#课程后台展示
class CourseAdmin(object):
    list_display = [
        'name',
        'desc',
        'detail',
        'degree',
        'learn_times',
        'students'
    ]
    search_fields = [
        'name',
        'desc',
        'detail',
        'degree',
        'students'
    ]
    list_filter = [
        'name',
        'desc',
        'detail',
        'degree',
        'learn_times',
        'students'
    ]

#课程
class LessonAdmin(object):
    list_display = [
        'course', 'name', 'add_time'
    ]
    search_fields = ['course', 'name']
    list_filter = ['course', 'name', 'add_time']

#视频
class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']

#课程资源
class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']

xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)