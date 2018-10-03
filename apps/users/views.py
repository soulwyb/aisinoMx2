from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse

from users.models import UserProfile, EmailVerifyRecord, Banner
from .froms import LoginForm, RegisterForm, ForgetForm, ActiveForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from utils.email_send import send_register_email
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course
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

            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = '欢迎注册吴玉斌小站'
            user_message.save()

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

#用户个人中心
class UserInfoView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'
    def get(self, request):
        return render(request, 'usercenter-info.html', {})
    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance = request.user)
        if user_info_form:
            user_info_form.save()

#用户修改头像
class UploadImageView(LoginRequiredMixin,View):
    login_url = '/login/'
    redirect_field_name = 'next'
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"', content_type='application/json')

#用户修改密码
class UpdatePwdView(LoginRequiredMixin,View):
    login_url = '/login/'
    redirect_field_name = 'next'
    def post(self, request):
        modiypwd_form = ModifyPwdForm(request.POST)
        if modiypwd_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'msg': '密码不一致，请重新输入'})
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"填写错误请检查"}', content_type='application/json')

#发送邮箱验证码
class SendEmailCodeView(View):
    def get(self, request):
        email = request.GET.get('email', '')

        if UserProfile.objects.filter(email = email):
            return HttpResponse('{"email":"邮箱已存在"}', content_type='application/json')
        send_register_email(email, 'update_email')
        return HttpResponse('{"status":"success"}', content_type='application/json')

#修改邮箱
class UpdateEmailView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed_records = EmailVerifyRecord.objects.filter(email = email, code = code, send_type= 'update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码无效"}', content_type='application/json')

#用户中心课程
class MyCourseView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        user_courses = UserCourse.objects.filter(user = request.user)
        return render(request, 'usercenter-mycourse.html', {
            'user_courses':user_courses
        })

#用户中心收藏机构
class MyFavOrgView(LoginRequiredMixin,View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user = request.user, fav_type = 2)
        for fav_org in fav_orgs:
            org_id = fav_orgs.fav_id
            org = CourseOrg.objects.get(id = org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html',{
            'org_list': org_list
        })

#用户中心收藏收藏老师
class MyFavTeacherView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user = request.user, fav_type = 3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id = teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list':teacher_list
        })

#用户中心收藏课程
class MyFavCourseView(LoginRequiredMixin,View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        course_list = []
        fav_courses =UserFavorite.objects.filter(user = request.user, fav_type = 1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id = course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'course_list': course_list
        })

#用户消息
class MyMessageView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, requset):
        all_message = UserMessage.objects.filter(user = requset.user.id)
        all_unread_messages = UserMessage.objects.filter(user = requset.user.id, has_read=False)
        for unread_messages in all_unread_messages:
            unread_messages.has_read = True
            unread_messages.save()

        try:
            page = requset.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_message, 4)
        message = p.page(page)
        return render(requset, 'usercenter-message.html', {
            'messsage': message
        })

#登出
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponse(reverse('index'))

#主页
class IndexView(View):
    def get(self, request):
        all_banner = Banner.objects.all().order_by('index')[:5]
        courses = Course.objects.filter(is_banner = False)[:6]
        banner_courses = Course.objects.filter(is_banner = True)[:3]
        course_org = CourseOrg.objects.all().order_by()[:6]
        return render(request, 'index.html',{
            'all_banner': all_banner,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_org': course_org
        })

def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response(
        "404.hml",{

        }
    )
    response.status_code = 404
    return response