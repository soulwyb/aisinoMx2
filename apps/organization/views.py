from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q
# Create your views here.

from .models import CourseOrg, CityDict, Teacher
from .froms import UserAskForm
from operation.models import UserFavorite
from courses.models import Course

#机构列表
class OrgView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_course = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(
                detail__icontains=search_keywords))

        #以城市筛选
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id = int(city_id))
        #以机构类别筛选(如果有选择城市,则是在所选城市的条件下在筛选机构类别
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category = category)
        #学习人数和课程数量排名
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')

        all_citys = CityDict.objects.all()
        org_nums = all_orgs.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        #从all_orgs中取5个数据， 每页显示5个
        p = Paginator(all_orgs, 3, request = request)
        orgs = p.page(page)

        hot_orgs = all_orgs.order_by("-click_num")[:4]

        return render(request, 'org-list.html', {
            'all_orgs' : orgs,
            'all_citys' : all_citys,
            'org_nums': org_nums,
            'city_id': city_id,
            'category': category,
            'hot_orgs': hot_orgs,
            'sort': sort,
            'search_keywords':search_keywords
        })

#用户的我要学习
class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit = True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"您的字段有错，请检查"}', content_type='application/json')

#机构详情主页
class OrgHomeView(View):
    '''
    机构首页
    '''
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id = int(org_id))
        course_org.click_num += 1
        course_org.save()
        all_courses = course_org.course_set.all()[:4]
        all_teacher = course_org.teacher_set.all()[:2]
        current_page = 'home'

        return  render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teacher': all_teacher,
            'course_org': course_org,
            'current_page': current_page
        })

#机构课程详情
class OrgCourseView(View):
    '''
    机构课程列表页
    '''
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id = int(org_id))
        all_courses = course_org.course_set.all()

        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org
        })

#机构描述
class OrgDescView(View):
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user = request.user, fav_id = course_org.id, fav_type = 2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'current_page': current_page,
            'course_org': course_org,
            'has_fav':has_fav
        })

#机构讲师
class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id = int(org_id))
        all_teachers = course_org.teacher_set.all()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user = request.user, fav_id = course_org.id, fav_type = 2):
                has_fav = True
        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'has_fav': has_fav,
            'current_page': current_page
        })

#收藏与取消收藏
class AddFavView(View):
    def post(self, request):
        id = request.POST.get('fav_id', 0)
        type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
        exist_records = UserFavorite.objects.filter(user = request.user, fav_id = int(id), fav_type= type)
        if exist_records:
            exist_records.delete()
            if int(type) == 1:
                course = Course.objects.get(id = int(id))
                course.fav_num -= 1
                if course.fav_num < 0:
                    course.fav_num = 0
                course.save()
            elif int(type) == 2:
                org = CourseOrg.objects.get(id = int(id))
                org.fav_num -= 1
                if org.fav_num < 0:
                    org.fav_num = 0
                org.save()
            elif int(type) == 3:
                teacher = Teacher.objects.get(id = int(id))
                teacher.fav_num -= 1
                if teacher.fav_num < 0:
                    teacher.fav_num = 0
                teacher.save()
            return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(type) == 1:
                course = Course.objects.get(id=int(id))
                course.fav_num += 1
                course.save()
            elif int(type) == 2:
                org = CourseOrg.objects.get(id=int(id))
                org.fav_num += 1
                org.save()
            elif int(type) == 2:
                teacher = Teacher.objects.get(id=int(id))
                teacher.fav_num += 1
                teacher.save()
            if int(type) > 0 and int(id) > 0:
                user_fav.fav_id = int(id)
                user_fav.fav_type = int(type)
                user_fav.user = request.user
                user_fav.save()
                return HttpResponse('{"status":"fail","msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"收藏出错"}', content_type='application/json')

class TeacherListView(View):
    def get(self, request):
        all_teacher = Teacher.objects.all()
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_course = all_teacher.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(
                detail__icontains=search_keywords))

        teacher_nums = all_teacher.count()

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_teacher = all_teacher.order_by('-click_nums')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        #从all_orgs中取5个数据， 每页显示5个
        p = Paginator(all_teacher, 3, request = request)
        orgs = p.page(page)
        rank_teacher = Teacher.objects.all().order_by('-fav_nums')[:5]
        return render(request, 'teachers-list.html', {
            'all_teacher':all_teacher,
            'teacher_nums':teacher_nums,
            'sort':sort,
            'rank_teachers':rank_teacher,
            'search_keywords': search_keywords
        })

class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id = int(teacher_id))
        teacher.click_num += 1
        teacher.save()
        all_course = teacher.course_set.all()
        rank_teacher = Teacher.objects.all().order_by('-fav_nums')[:5]
        has_fav_teacher = False
        if UserFavorite.objects.filter(user = request.user, fav_id = teacher_id, fav_type=3):
            has_fav_teacher = True
        has_fav_org = False
        if UserFavorite.objects.filter(user = request.user, fav_id = teacher.org.id, fav_type = 2):
            has_fav_org = True
        return render(request, 'teacher-detail.html', {
            'teacher':teacher,
            'all_course':all_course,
            'rank_teachers': rank_teacher,
            'has_fav_teacher':has_fav_teacher,
            'has_fav_org':has_fav_org,
        })

