from datetime import datetime

from django.db import models

from organization.models import CourseOrg, Teacher

# Create your models here.

#课程信息表
class Course(models.Model):
    DEGREE_CHOICES = (
        ('cj', u'初级'),
        ('zj', u'中级'),
        ('gj', u'高级')
    )

    name = models.CharField(max_length=50, verbose_name=u'课程名')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    detail = models.TextField(verbose_name=u'课程详情')
    course_org = models.ForeignKey(CourseOrg, verbose_name=u'所属机构', null = True, blank= True, on_delete= models.CASCADE)
    degree = models.CharField(choices=DEGREE_CHOICES, verbose_name=u'难度', max_length=2)
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长(分钟数)')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    tag = models.CharField(max_length=15, verbose_name=u'课程标签', default='')
    image = models.ImageField(
        upload_to="courses/%Y/%m",
        verbose_name=u'封面图',
        max_length=100
    )
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    category = models.CharField(max_length=20, default=u'', verbose_name = u'课程类别')
    teacher = models.ForeignKey(Teacher, verbose_name=u'讲师', null = True, blank=True, on_delete=models.CASCADE)
    you_need_know = models.CharField(max_length=300, default=u'一颗勤学的心是本课程必要前提', verbose_name=u'课程须知')
    teacher_tell = models.CharField(max_length=300, default=u'按时交作业，不然叫家长', verbose_name=u'老师告诉你')
    is_banner = models.BooleanField(default=False, verbose_name=u'是否轮播')

    class Meta:
        verbose_name = u'课程信息'
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        return self.lesson_set.all().count()

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def get_teacher_nums(self):
        return self.teacher_set.all().count

    def __str__(self):
        return self.name

#章节
class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    url = models.CharField(max_length=200, default="http://www.baidu.com", verbose_name=u'访问地址')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

#视频(每章视频)
class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长(分钟数)')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

#课程资源
class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u'名称')
    download = models.FileField(
        upload_to="course/rescourse/%Y/%m",
        verbose_name=u'资源文件',
        max_length=100
    )
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name