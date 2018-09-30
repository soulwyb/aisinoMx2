from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Course, CourseResource, Video
from operation.models import UserFavorite, CourseComments, UserCourse

# Create your views here.


class CourseListView(View):
    def get(self, request):
        all_course = Course.objects.all()

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_course = all_course.order_by('-students')
            elif sort == 'courses':
                all_course = all_course.order_by('-click_nums')
        hot_course = Course.objects.all().order_by('-students')[:3]
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_course, 6, request = request)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_course': courses,
            'sort': sort,
            'hot_courses': hot_course
        })

#课程详情
class CourseDetialView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id = int(course_id))
        course.click_nums += 1
        course.save()
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag = tag)[1:2]
        else:
            relate_courses = []

        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id = course_id, fav_type= 1):
                has_fav_course = True
            if UserFavorite.objects.filter(user = request.user, fav_id = course.course_org.id, fav_type = 2):
                has_fav_org = True
        return render(request, 'course-detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org
        })

#章节详情
class CourseInfoView(View, LoginRequiredMixin):
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    def get(self, request, course_id):
        course = Course.objects.get(id = int(course_id))
        all_resources = CourseResource.objects.filter(course = course)
        user_courses = UserCourse.objects.filter(course = course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in = user_ids)
        course_ids = [all_user_course.course.id for all_user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in = course_ids).order_by('-click_nums')[:5]
        return render(request, 'course-video.html', {
            'course':course,
            'all_resources': all_resources
        })

#课程评论
class CommentsView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id = int(course_id))
        all_resources = CourseResource.objects.filter(course= course)
        all_comments = CourseComments.objects.filter(course = course).order_by('-add_time')
        user_courses = UserCourse.objects.filter(course = course)
        user_ids = [user_course.user_id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in = user_ids)
        course_ids = [user_course.course_id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in = course_ids).order_by('-click.nums').exclude(id = course.id)[:4]
        return render(request, 'course-comment.html', {
            'course': course,
            'all_resources': all_resources,
            'all_comments': all_comments,
            'relate_courses':relate_courses
        })

class AddCommentsView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if int(course_id) > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id = int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.save()
            return HttpResponse('{"status":"success","msg":"评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"评论失败"}', content_type='application/json')


class VideoPlayView(View, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'next'
    def get(self, request, video_id):
        video = Video.objects.get(id = int(video_id))
        course = Video.lesson.course
        user_courses = UserCourse.objects.filter(user = request.user, course = course)
        if not user_courses:
            user_course = UserCourse(user = request.user, course = course)
            user_course.save()
        all_resources = CourseResource.objects.filter(course = course)
        user_courses = UserCourse.objects.filter(course = course)
        user_ids = [user_course.user_id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in = user_ids)
        course_ids = [user_course.course_id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in = course_ids).order_by('-click.nums').exclude(id = course.id)
        return render(request, 'course-play.html', {
            'course': course,
            'all_resources': all_resources,
            'relate_courses': relate_courses,
            'video': video
        })