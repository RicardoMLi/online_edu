from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse

from .forms import UserAskForm
from .models import UserFav,CourseComment

from course.models import Course
from organization.models import CourseOrganization,Teacher
from utils.mixin_utils import LoginRequiredMixin

class UserAskView(View):
	"""
	用户咨询
	"""
	def post(self,request):
		userask_form = UserAskForm(request.POST)
		response_data = {}

		if userask_form.is_valid():
			userask_form.save(commit=True)
			response_data['status'] = 'success'
		else:
			response_data['status'] = 'fail'
			response_data['msg'] = '添加出错'

		return JsonResponse(response_data)

class UserFavView(View):
	"""
	用户收藏,取消收藏
	"""
	def post(self,request):
		fav_id = int(request.POST.get('fav_id','0'))
		fav_type = int(request.POST.get('fav_type','0'))
		response_data = {}

		#判断用户是否登录
		if not request.user.is_authenticated:
			response_data['status'] = 'fail'
			response_data['msg'] = '用户未登录'

			return JsonResponse(response_data)

		is_existed = UserFav.objects.filter(user=request.user,fav_id=fav_id,fav_type=fav_type)

		#若存在，则取消收藏
		if is_existed:
			#将收藏量-1
			if fav_type == 1:
				course = Course.objects.get(id=fav_id)
				course.fav_num = course.fav_num-1 if course.fav_num > 0 else 0
				course.save()
			elif fav_type == 2:
				organization = CourseOrganization.objects.get(id=fav_id)
				organization.fav_num = organization.fav_num-1 if organization.fav_num > 0 else 0
				organization.save()
			elif fav_type == 3:
				teacher = Teacher.objects.get(id=fav_id)
				teacher.fav_num = teacher.fav_num-1 if teacher.fav_num > 0 else 0
				teacher.save()
			else:
				pass

			is_existed.delete()
			response_data['status'] = 'success'
			response_data['msg'] = '收藏'

		else:
			if fav_id > 0 and fav_type > 0:
				user_fav = UserFav()
				user_fav.user = request.user
				user_fav.fav_id = fav_id
				user_fav.fav_type = fav_type
				user_fav.save()
				#将收藏量+1
				if fav_type == 1:
					course = Course.objects.get(id=fav_id)
					course.fav_num += 1
					course.save()
				elif fav_type == 2:
					organization = CourseOrganization.objects.get(id=fav_id)
					organization.fav_num += 1
					organization.save()
				elif fav_type == 3:
					teacher = Teacher.objects.get(id=fav_id)
					teacher.fav_num += 1
					teacher.save()
				else:
					pass
				response_data['status'] = 'success'
				response_data['msg'] = '已收藏'
			else:
				response_data['status'] = 'fail'
				response_data['msg'] = '收藏出错'

		return JsonResponse(response_data)

class CommentView(LoginRequiredMixin,View):

	def post(self,request):
		course_id = int(request.POST.get('course_id','0'))
		comment = request.POST.get('comment','')
		response_data = {}

		#判断用户是否登录
		if not request.user.is_authenticated:
			response_data['status'] = 'fail'
			response_data['msg'] = '用户未登录'

			return JsonResponse(response_data)

		if course_id > 0 and comment:
			course_comment = CourseComment()
			course = Course.objects.filter(id=course_id)

			if not course:
				response_data['status'] = 'fail'
				response_data['msg'] = '评论的课程不存在'

			course_comment.course = course[0]
			course_comment.user = request.user
			course_comment.comment = comment
			course_comment.save()
			response_data['status'] = 'success'
			response_data['msg'] = '评论成功'
		else:
			response_data['status'] = 'fail'
			response_data['msg'] = '评论失败'

		return JsonResponse(response_data)

