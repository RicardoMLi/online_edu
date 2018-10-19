from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.base import View

from course.models import Course
from user.models import UserProfile
from utils.mixin_utils import LoginRequiredMixin

class OrderInfoView(LoginRequiredMixin,View):

	def get(self,request,info):
		context = {}
		if info == '':
			return render(request,'404.html',context)
		if '_' not in info:
			return render(request,'404.html',context)
		user_id = int(info.split('_')[0])
		course_id = int(info.split('_')[1])

		if not (Course.objects.filter(id=course_id).exists() and UserProfile.objects.filter(id=user_id).exists()):
			return render(request,'404.html',context)

		course = Course.objects.get(id=course_id)
		context['course'] = course

		return render(request,'trade/order.html',context)

