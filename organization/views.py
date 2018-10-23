from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.core.cache import cache
from django.views.generic import View
from pure_pagination import Paginator,EmptyPage,PageNotAnInteger

from .models import CourseOrganization,CityDict,Teacher

from Mxonline.settings import MAX_CACHE_TIME
from course.models import Course
from user_operation.models import UserFav

class OrganizationListView(View):

	def get(self,request):
		context = {}
		all_orgs = CourseOrganization.objects.all()
		hot_orgs = cache.get('hot_orgs')
		if hot_orgs is None:
			hot_orgs = CourseOrganization.objects.order_by('-click_num')[:4]
			cache.set('hot_orgs',hot_orgs,MAX_CACHE_TIME)

		all_cities = cache.get('all_cities')
		if all_cities is None:
			all_cities = CityDict.objects.all()
			cache.set('all_cities',all_cities,MAX_CACHE_TIME)

		#搜索课程机构
		keywords = request.GET.get('keywords','')
		if keywords:
			all_orgs = all_orgs.filter(Q(name__icontains=keywords)|Q(desc__icontains=keywords)|Q(address__icontains=keywords))

		#根据所在城市筛选课程机构
		city_id = request.GET.get('city','')
		if city_id:
			all_orgs = all_orgs.filter(city_id=int(city_id))

		#根据机构类别筛选课程机构
		category = request.GET.get('category','')
		if category:
			all_orgs = all_orgs.filter(category=category)

		#根据收藏量和学习人数排序
		sort = request.GET.get('sort','')
		if sort:
			if sort == 'students_num':
				all_orgs = all_orgs.order_by('-students_num')
			elif sort == 'fav_num':
				all_orgs = all_orgs.order_by('-fav_num')
			else:
				pass

		#分页
		try:
			page = request.GET.get('page',1)
		except PageNotAnInteger:
			page = 1

		p = Paginator(all_orgs,5,request=request)

		organizations = p.page(page)

		context['organizations'] = organizations
		context['all_cities'] = all_cities
		context['hot_orgs'] = hot_orgs
		context['org_nums'] = all_orgs.count()
		context['city_id'] = city_id
		context['category'] = category
		context['sort'] = sort
		return render(request,'organization/org-list.html',context)

class OrganizationHomeView(View):

	def get(self,request,organization_id):
		context = {}
		#以防用户输入错误机构id导致出错
		course_org = None
		#判断用户是否收藏本机构
		has_fav = False

		try:
			course_org = CourseOrganization.objects.get(id=organization_id)
			course_org.click_num += 1 
			course_org.save()
		except Exception:
			return render(request,'404.html',context)
		
		if request.user.is_authenticated:
			if UserFav.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
				has_fav = True

		#取三门课程
		all_courses = course_org.course_set.all()[:3]
		#取两名讲师
		all_teachers = course_org.teacher_set.all()[:2]

		context['current_page'] = 'home'
		context['has_fav'] = has_fav
		context['course_org'] = course_org
		context['all_courses'] = all_courses
		context['all_teachers'] = all_teachers

		return render(request,'organization/org-detail-homepage.html',context)

class OrganizationCourseView(View):

	def get(self,request,organization_id):
		context = {}
		#以防用户输入错误机构id导致出错
		course_org = None
		#判断用户是否收藏本机构
		has_fav = False

		try:
			course_org = CourseOrganization.objects.get(id=organization_id)
		except Exception:
			return render(request,'404.html',context)

		if request.user.is_authenticated:
			if UserFav.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
				has_fav = True

		all_courses = course_org.course_set.all()

		context['current_page'] = 'course'
		context['has_fav'] = has_fav
		context['course_org'] = course_org
		context['all_courses'] = all_courses

		return render(request,'organization/org-detail-course.html',context)

class OrganizationTeacherView(View):

	def get(self,request,organization_id):
		context = {}
		#以防用户输入错误机构id导致出错
		course_org = None
		#判断用户是否收藏本机构
		has_fav = False

		try:
			course_org = CourseOrganization.objects.get(id=organization_id)
		except Exception:
			return render(request,'404.html',context)

		if request.user.is_authenticated:
			if UserFav.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
				has_fav = True

		all_teachers = course_org.teacher_set.all()

		context['has_fav'] = has_fav
		context['current_page'] = 'teacher'
		context['course_org'] = course_org
		context['all_teachers'] = all_teachers

		return render(request,'organization/org-detail-teachers.html',context)

class OrganizationDescriptionView(View):

	def get(self,request,organization_id):
		context = {}
		#以防用户输入错误机构id导致出错
		course_org = None
		#判断用户是否收藏本机构
		has_fav = False

		try:
			course_org = CourseOrganization.objects.get(id=organization_id)
		except Exception:
			return render(request,'404.html',context)

		if request.user.is_authenticated:
			if UserFav.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
				has_fav = True

		context['current_page'] = 'desc'
		context['has_fav'] = has_fav
		context['course_org'] = course_org

		return render(request,'organization/org-detail-desc.html',context)

class TeacherListView(View):

	def get(self,request):
		context = {}
		all_teachers = Teacher.objects.all()
		hot_teachers = cache.get('hot_teachers')
		if hot_teachers is None:
			hot_teachers = all_teachers.order_by('-click_num')[:5]
			cache.set('hot_teachers',hot_teachers,MAX_CACHE_TIME)

		#搜索讲师
		keywords = request.GET.get('keywords','')
		if keywords:
			all_teachers = all_teachers.filter(Q(name__icontains=keywords)|Q(work_company__icontains=keywords)|Q(work_position__icontains=keywords))

		#根据收藏量和学习人数排序
		sort = request.GET.get('sort','')
		if sort:
			if sort == 'hot':
				all_teachers = all_teachers.order_by('-click_num')
			elif sort == 'work_years':
				all_teachers = all_teachers.order_by('-work_years')
			else:
				pass

		#分页
		try:
			page = request.GET.get('page',1)
		except PageNotAnInteger:
			page = 1

		p = Paginator(all_teachers,5,request=request)

		teachers = p.page(page)

		context['sort'] = sort
		context['teachers'] = teachers
		context['hot_teachers'] = hot_teachers

		return render(request,'organization/teachers-list.html',context)

class TeacherDetailView(View):

	def get(self,request,teacher_id):
		context = {}
		has_teacher_fav = False
		has_org_fav = False
		teacher = None
		#防止用户输入错误讲师id
		try:
			teacher = Teacher.objects.get(id=teacher_id)
			teacher.click_num += 1
			teacher.save()
		except Exception:
			return render(request,'404.html',context)

		if request.user.is_authenticated:
			if UserFav.objects.filter(user=request.user,fav_id=teacher.id,fav_type=3):
				has_teacher_fav = True
			if UserFav.objects.filter(user=request.user,fav_id=teacher.organization.id,fav_type=2):
				has_org_fav = True

		context['teacher'] = teacher
		context['has_teacher_fav'] = has_teacher_fav
		context['has_org_fav'] = has_org_fav
		context['all_courses'] = Course.objects.filter(teacher=teacher)
		context['hot_teachers'] = Teacher.objects.all().order_by('-click_num')[:5]

		return render(request,'organization/teacher-detail.html',context)


