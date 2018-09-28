from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

from .models import CourseOrg, CityDict

#机构列表
class OrgView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()

        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id = int(city_id))

        all_citys = CityDict.objects.all()
        org_nums = all_orgs.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        #从all_orgs中取5个数据， 每页显示5个
        p = Paginator(all_orgs, 3, request = request)
        orgs = p.page(page)


        return render(request, 'org-list.html', {
            'all_orgs' : orgs,
            'all_citys' : all_citys,
            'org_nums': org_nums,
            'city_id': city_id,
        })