from django.shortcuts import render,render_to_response
from django.views.generic import View
from django.core.cache import cache

from .settings import MAX_CACHE_TIME

from user.models import Banner
from course.models import Course
from organization.models import CourseOrganization

class IndexView(View):

	def get(self,request):
		context = {}
		#首页数据缓存
		banners = cache.get('banners')
		if banners is None:
			banners = Banner.objects.all().order_by('index')
			cache.set('banners',banners,MAX_CACHE_TIME)

		banner_courses = cache.get('banner_courses')
		if banner_courses is None:
			banner_courses = Course.objects.filter(is_banner=True)
			cache.set('banner_courses',banner_courses,MAX_CACHE_TIME)

		courses = cache.get('courses')
		if courses is None:
			courses = Course.objects.filter(is_banner=False)[:6]
			cache.set('courses',courses,MAX_CACHE_TIME)

		course_orgs = cache.get('course_orgs')
		if course_orgs is None:
			course_orgs = CourseOrganization.objects.all()[:15]
			cache.set('course_orgs',course_orgs,MAX_CACHE_TIME)

		context['banners'] = banners
		context['courses'] = courses
		context['banner_courses'] = banner_courses
		context['course_orgs'] = course_orgs
		
		return render(request,'index.html',context)

def page_not_found(request):
	response = render_to_response('404.html',{})
	response.status_code = 404

	return response

def page_error(request):
	response = render_to_response('500.html', {})
	response.status_code = 500

	return response