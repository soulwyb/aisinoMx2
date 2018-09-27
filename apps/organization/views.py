from django.shortcuts import render
from django.views.generic.base import View
# Create your views here.

from .models import CourseOrg, CityDict

#机构列表
class OrgView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()
        return render(request, 'org-list.html', {
            'all_orgs' : all_orgs,
            'all_citys' : all_citys
        })