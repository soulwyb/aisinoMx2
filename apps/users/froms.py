# encoding:utf-8
__author__ = 'wuyubin'
__date__ = '2018-09-26 13:32'

from django import forms
from captcha.fields import CaptchaField

#验证码form&注册表单
class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})

#激活表单验证
class ActiveForm(forms.Form):
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})

#登录的表单内容格式验证（不经过数据库，先看格式对不对
class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)