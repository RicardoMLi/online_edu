from django.shortcuts import render
from django.db.models import Q
from django.views.generic import View
from pure_pagination import Paginator,PageNotAnInteger,EmptyPage

from .models import Course,CourseResource,Video

from user_operation.models import UserFav,CourseComment,UserCourse
from utils.mixin_utils import LoginRequiredMixin

class CourseListView(View):

	def get(self,request):
		context = {}
		all_courses = Course.objects.all().order_by('-created_time')

		#课程搜索
		keywords = request.GET.get('keywords','')
		if keywords:
			all_courses = all_courses.filter(Q(name__icontains=keywords)|Q(short_desc__icontains=keywords)|Q(detail_desc__icontains=keywords))

		sort = request.GET.get('sort','')
		if sort:
			if sort == 'hot':
				all_courses = all_courses.order_by('-click_num')
			elif sort == 'students':
				all_courses = all_courses.order_by('-students_num')
			else:
				pass
		#分页
		try:
			page = request.GET.get('page',1)
		except PageNotAnInteger:
			page = 1

		p = Paginator(all_courses,6,request=request)

		courses = p.page(page)
		context['sort'] = sort
		context['all_courses'] = courses
		context['hot_courses'] = all_courses.order_by('-click_num')[:3]

		return render(request,'course/course-list.html',context)

class CourseDetailView(View):

	def get(self,request,course_id):
		context = {}
		#以防用户输入错误课程id导致出错
		course = None
		#判断用户是否收藏本机构
		has_fav_course = False
		has_fav_org = False
		try:
			course = Course.objects.get(id=course_id)
			course.click_num += 1
			course.save()
		except Exception as e:
			return render(request,'404.html',context)

		if request.user.is_authenticated:
			if UserFav.objects.filter(user=request.user,fav_id=course.id,fav_type=1):
				has_fav_course = True
			if UserFav.objects.filter(user=request.user,fav_id=course.course_org.id,fav_type=2):
				has_fav_org = True
		#查找相关课程
		tag = course.tag
		if tag:
			related_courses = Course.objects.filter(tag=tag)[:2]
			context['related_courses'] = related_courses

		context['course'] = course
		context['has_fav_course'] = has_fav_course
		context['has_fav_org'] = has_fav_org

		return render(request,'course/course-detail.html',context)

class CourseInfoView(LoginRequiredMixin,View):

	def get(self,request,course_id):
		context = {}
		#以防用户输入错误课程id导致出错
		course = None
		try:
			course = Course.objects.get(id=course_id)
			course.students_num += 1
			course.save()
		except Exception as e:
			return render(request,'404.html',context)

		#若学生第一次学习本课程,则将课程与学生关联
		user_course = UserCourse.objects.filter(user=request.user,course=course)
		if not user_course:
			user_course = UserCourse()
			user_course.user = request.user
			user_course.course = course
			user_course.save()

		#查找所有课程资料
		course_resources = CourseResource.objects.filter(course=course)

		#查找学习过本课程的同学还学习了其他什么课程
		user_ids = [user_course.user.id for user_course in UserCourse.objects.filter(course=course)]
		related_courses = [user_course.course for user_course in UserCourse.objects.filter(user_id__in=user_ids)]
		#根据课程名去重
		related_courses = list(set(related_courses))[:3]
		context['course'] = course
		context['course_resources'] = course_resources
		context['related_courses'] = related_courses

		return render(request,'course/course-video.html',context)

class CourseCommentView(LoginRequiredMixin,View):

	def get(self,request,course_id):
		context = {}
		#以防用户输入错误课程id导致出错
		course = None
		try:
			course = Course.objects.get(id=course_id)
			course.click_num += 1
			course.save()
		except Exception as e:
			return render(request,'404.html',context)

		all_comments = CourseComment.objects.filter(course=course).order_by('-created_time')
		#查找所有课程资料
		course_resources = CourseResource.objects.filter(course=course)
		context['course'] = course
		context['all_comments'] = all_comments
		context['course_resources'] = course_resources

		return render(request,'course/course-comment.html',context)

class VideoPlayView(View):

	def get(self,request,video_id):
		context = {}
		video = Video.objects.get(id=video_id)
		course = video.chapter.course
		
		#若学生第一次学习本课程,则将课程与学生关联
		user_course = UserCourse.objects.filter(user=request.user,course=course)
		if not user_course:
			user_course = UserCourse()
			user_course.user = request.user
			user_course.course = course
			user_course.save()

		#查找所有课程资料
		course_resources = CourseResource.objects.filter(course=course)

		#查找学习过本课程的同学还学习了其他什么课程
		user_ids = [user_course.user.id for user_course in UserCourse.objects.filter(course=course)]
		related_courses = [user_course.course for user_course in UserCourse.objects.filter(user_id__in=user_ids)]
		#根据课程名去重
		related_courses = list(set(related_courses))[:3]
		context['course'] = course
		context['video'] = video
		context['course_resources'] = course_resources
		context['related_courses'] = related_courses

		return render(request,'course/video-play.html',context)

