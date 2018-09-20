from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

#用户中心（info）
class UserProfile(AbstractUser):
    GREDER_CHOICES = (
        ('male', u'男'),
        ('female', u'女')
    )
#依次为 昵称，生日，性别，地址，手机号，头像
    nick_name = models.CharField(max_length=50, verbose_name=u'昵称', default='')
    birthday = models.DateField(verbose_name=u'生日', null = True, blank= True)
    gender = models.CharField(
        max_length=5,
        verbose_name=u'性别',
        default = 'female',
        choices= GREDER_CHOICES
    )
    address = models.CharField(max_length=100, verbose_name=u'地址', default='')
    mobile = models.CharField(max_length=11, null = True, blank = True)
    image = models.ImageField(
        upload_to='image/%Y/%m',
        default=u'image/default.jpg',
        max_length=100
    )

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

#邮箱验证码
class EmailVerifyRecord(models.Model):
    SEND_CHOICES = (
        ('register', u'注册'),
        ('forget', u'找回密码')
    )

    code = models.CharField(max_length=20, verbose_name=u'验证码')
    email = models.EmailField(max_length=50, verbose_name=u'邮箱')
    send_type = models.CharField(choices= SEND_CHOICES, max_length=10, verbose_name=u'发送类型')
    send_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u'y邮箱验证码'
        verbose_name_plural = verbose_name

#轮播图
class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u'标题')
    image = models.ImageField(
        upload_to= "banner/%Y/%m",
        verbose_name=u'轮播图',
        max_length=100
    )
    url = models.URLField(max_length=200, verbose_name=u'访问地址')
    #index是指轮播图的下标顺序，数值越大越后面播放
    index = models.IntegerField(default=100, verbose_name=u'顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'轮播图'
        verbose_name_plural = verbose_name