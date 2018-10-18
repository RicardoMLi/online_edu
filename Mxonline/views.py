from django.shortcuts import render,render_to_response
from django.views.generic import View

from user.models import Banner
from course.models import Course
from organization.models import CourseOrganization

class IndexView(View):

	def get(self,request):
		context = {}
		banners = Banner.objects.all().order_by('index')
		banner_courses = Course.objects.filter(is_banner=True)
		courses = Course.objects.filter(is_banner=False).order_by('-click_num')[:6]
		course_orgs = CourseOrganization.objects.all().order_by('-click_num')[:15]

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