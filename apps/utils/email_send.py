# encoding:utf-8
__author__ = 'wuyubin'
__date__ = '2018-09-26 14:20'

from random import Random

from django.core.mail import send_mail, EmailMessage
from aisinoMx.settings import EMAIL_FROM
from django.template.loader import render_to_string

from users.models import EmailVerifyRecord

def random_str(random_length = 8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0, length)]#为啥不直接choces?
    return str

def send_register_email(email, send_type = 'register'):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type

    email_record.save()

    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = u'吴玉斌小站 注册连接'
        email_body = u'请点击一下连接激活你的账号：http://127.0.0.1:8000/active/{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

        if send_status:
            pass
    elif send_type == 'forget':
        email_title = u'吴玉斌小站 找回密码连接'
        #render_to_string将html页面与数据打包在一起
        email_body = render_to_string(
            'email_forget.html',
            {
                'active_code': code
            }
        )
        #使用EmailMessage来发送邮件的原因是，可以用更多拓展的功能，其实send_mail函数也是调用这个类来发送邮件的
        msg = EmailMessage(email_title, email_body, EMAIL_FROM, [email])
        msg.content_subtype = 'html'
        send_status = msg.send()