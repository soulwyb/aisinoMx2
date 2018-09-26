from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.views.generic.base import View

from users.models import UserProfile, EmailVerifyRecord
from .froms import LoginForm, RegisterForm
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
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')

            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name

            user_profile.password = make_password(pass_word)
            user_profile.is_active = False
            user_profile.save()
            send_register_email(user_name, 'register')

            return render(request, 'login.html')

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
                login(user)
                return render(request, 'index.html')
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