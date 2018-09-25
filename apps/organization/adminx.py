# encoding:utf-8
__author__ = 'wuyubin'
__date__ = '2018-09-25 14:04'

from .models import CityDict, CourseOrg, Teacher
import xadmin

#城市
class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']

#课程机构
class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_num', 'fav_nums', 'add_time']
    search_fields = ['name', 'desc', 'click_num', 'fav_nums']
    list_filter = ['name', 'desc', 'click_num', 'fav_nums', 'add_time']

#讲师
class TeacherAdmin(object):
    list_display = ['name', 'org', 'work_years', 'work_company', 'add_time']
    search_fields = ['name', 'org', 'work_years', 'work_company']
    list_filter = ['name', 'org', 'work_years', 'work_company', 'add_time']

xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(Teacher, TeacherAdmin)