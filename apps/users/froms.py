# encoding:utf-8
__author__ = 'wuyubin'
__date__ = '2018-09-26 13:32'

from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile

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

#忘记密码表单
class ForgetForm(forms.Form):
    email = forms.EmailField(required = True)
    captcha = CaptchaField(error_messages = {'invalid': u'验证码错误'})

#修改密码
class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)

class UploadImageForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['image']

class UserInfoForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birthday', 'address', 'mobile']