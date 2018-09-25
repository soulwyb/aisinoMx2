# encoding:utf-8
__author__ = 'wuyubin'
__date__ = '2018-09-25 13:33'

import xadmin
from xadmin import views

from .models import EmailVerifyRecord, Banner

#邮箱验证码
class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']

xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)

#轮播图
class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


class BaseSetting(object):
    #开启主题功能
    enable_themes = True
    use_bootswatch = True

class GlobalSetting(object):
    site_title = '吴玉斌：后台管理'
    site_footer = "aisino's mooc"
    #收起菜单
    menu_style = 'accordion'

xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(Banner, BannerAdmin)