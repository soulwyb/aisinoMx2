# encoding:utf-8
__author__ = 'wuyubin'
__date__ = '2018-09-26 14:20'

from random import Random

from django.core.mail import send_mail
from aisinoMx.settings import EMAIL_FROM

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
        email_title = '吴玉斌小站 注册连接'
        email_body = '请点击一下连接激活你的账号：http://127.0.0.1:80000/active/{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

        if send_status:
            pass
    elif send_type == 'forget':
        email_title = '吴玉斌小站 找回密码连接'
        email_body = loader.render_to_string(
            'email_forget.html',
            {
                'active_code': code
            }
        )