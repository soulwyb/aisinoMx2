from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

from .models import CourseOrg, CityDict

#机构列表
class OrgView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        #以城市筛选
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id = int(city_id))
        #以机构类别筛选(如果有选择城市,则是在所选城市的条件下在筛选机构类别
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category = category)

        all_citys = CityDict.objects.all()
        org_nums = all_orgs.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        #从all_orgs中取5个数据， 每页显示5个
        p = Paginator(all_orgs, 3, request = request)
        orgs = p.page(page)

        hot_orgs = all_orgs.order_by("-click_num")[:3]

        return render(request, 'org-list.html', {
            'all_orgs' : orgs,
            'all_citys' : all_citys,
            'org_nums': org_nums,
            'city_id': city_id,
            'category': category,
            'hot_orgs': hot_orgs
        })