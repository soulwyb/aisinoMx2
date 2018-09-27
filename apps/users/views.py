from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.views.generic.base import View

from users.models import UserProfile, EmailVerifyRecord
from .froms import LoginForm, RegisterForm, ForgetForm, ActiveForm, ModifyPwdForm
from utils.email_send import send_register_email
# Create your views here.

#用户注册
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html',{'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(email = user_name):
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已存在'})
            pass_word = request.POST.get('password', '')

            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name

            user_profile.password = make_password(pass_word)
            user_profile.is_active = False
            user_profile.save()
            send_register_email(user_name, 'register')

            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})

#用户激活
class ActiveUserView(View):
    def get(self, request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code = active_code)
        active_form = ActiveForm(request.GET)

        if all_record:
            for record in all_record:
                email = record.email
                user = UserProfile.objects.get(email = email)
                user.is_active = True
                user.save()
                return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'msg':'您的激活连接无效',"active_form":active_form})

#用户登录（类)
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        #先验证下表单中内容的格式有没有错
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')

            user = authenticate(username = user_name, password = pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg': '用户名未激活，请前往邮箱进行激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})

        else:
            return render(request, 'login.html', {'login_form': login_form})

#用户登录(函数
def user_login(request):
    if request.method == 'POST':
        user_name = request.POST.get('username', '')
        pass_word = request.POST.get('password', '')
        #Django自带验证，成功放回User对象 失败返回None
        user = authenticate(username = user_name, password = pass_word)
        if user is not None:
            login(request, user)
            return render(request, 'index.html')
        else:
            return render(request, 'login.html', {"msg":'用户名或密码错误'})

    elif request.method == 'GET':
        return render(request, 'login.html', {})

#重载变量，使用户名和邮箱均可登陆
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username = username) | Q(email = username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

#忘记密码
class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'forget')
            return render(request, 'login.html', {'msg': '重置密码邮件已发送，请注意查收'})
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})

#重置密码
class ResetView(View):
    def get(self, request, active_code):
        all_recode = EmailVerifyRecord.objects.filter(code = active_code)
        active_form = ActiveForm(request.GET)
        if all_recode:
            EmailVerifyRecord.objects.filter(code = active_code).delete()
            for recode in all_recode:
                email = recode.email
                return render(request, 'password_reset.html', {'email':email})
        else:
            return render(request, 'forgetpwd.html', {'msg': '您的重置密码连接无效，请重新请求', 'active_form': active_form})

#修改密码
class ModifyPwdView(View):
    def post(self, request):
        modifypwd_form = ModifyPwdForm(request.POST)
        if modifypwd_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')

            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'msg': '密码不一致，请重新输入'})
            user = UserProfile.objects.get(email = email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, 'login.html', {'msg': '密码修改成功，请登录'})
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'modiypwd_form': modifypwd_form})