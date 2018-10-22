import re
import random

from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth import login,logout
from django.contrib.auth.backends import ModelBackend
from django.views.generic.base import View
from pure_pagination import PageNotAnInteger,Paginator,EmptyPage

from .models import UserProfile,EmailVerifyRecord,MobileVerifyRecord
from .forms import LoginForm,RegisterForm,ForgetPasswordForm,ModifyPasswordForm,ModifyUserAvaterForm,UserInfoForm
from Mxonline.settings import REGEX_MOBILE,SMS_CODE_EXPIRES_SECONDS
from user_operation.models import UserCourse,UserFav,UserMessage
from course.models import Course
from trade.models import Order
from organization.models import CourseOrganization,Teacher
from utils.email_send import send_email
from utils.mixin_utils import LoginRequiredMixin
from utils.yuntongxun.SendTemplateSMS import ccp


class CustomBackend(ModelBackend):

	def authenticate(self,username=None,password=None,**kwargs):
		try:
			user = UserProfile.objects.get(Q(username=username)|Q(email=username))
			if user.check_password(password):
				return user
		except Exception as e:
			return None


class LoginView(View):

	def get(self,request):
		context = {}
		return render(request, 'user/login.html', context)

	def post(self,request):
		context = {}
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			user = login_form.cleaned_data['user']
			login(request,user)
			return redirect(request.GET.get('from',reverse('index')))
		else:
			context['login_form'] = login_form
			return render(request,'user/login.html',context)

class LogoutView(View):

	def get(self,request):
		logout(request)
		#跳转上一次页面
		return redirect(request.GET.get('from',reverse('index'))) 

class ActiveUserView(View):

	def get(self,request,active_code):
		all_records = EmailVerifyRecord.objects.filter(code=active_code)
		if all_records:
			for record in all_records:
				email = record.email
				user = UserProfile.objects.get(email=email)
				user.is_active = True
				user.save()
				#删除注册账号时发生的验证码记录
				for record in EmailVerifyRecord.objects.filter(email=email,send_type='register'):
					record.delete()
			return render(request,'index.html',context={})
		else:
			return render(request,'user/active_fail.html',context={})

class RegisterView(View):

	def get(self,request):
		context = {}
		context['register_form'] = RegisterForm()
		return render(request,'user/register.html',context)

	def post(self,request):
		context = {}
		register_form = RegisterForm(request.POST)
		if register_form.is_valid():
			email = register_form.cleaned_data['email']
			#发送激活邮件
			return_msg = send_email(email,'register')
			if return_msg == '':
				#用户注册
				username = register_form.cleaned_data['email']
				password = register_form.cleaned_data['password']
				user = UserProfile.objects.create_user(username,email,password)
				user.is_active = False
				user.save()
				#发送欢迎消息
				message = UserMessage()
				message.user = user.id
				message.message = "欢迎注册慕学在线网,希望您学习愉快。"
				message.has_read = False
				message.save()
				#用户登录
				login(request,user)
				return redirect('login')
			elif return_msg == '邮箱地址错误':
				context['title'] = '邮箱地址错误'
				return render(request,'user/send_response.html',context)
			else:
				context['title'] = '网络连接失败'
				return render(request,'user/send_response.html',context)
		else:
			context['register_form'] = register_form
			return render(request,'user/register.html',context)

class ForgetPasswordView(View):

	def get(self,request):
		context = {}
		context['forget_form'] = ForgetPasswordForm()
		return render(request,'user/forgetpwd.html',context)

	def post(self,request):
		context = {}
		forget_form = ForgetPasswordForm(request.POST)

		if forget_form.is_valid():
			email = forget_form.cleaned_data['email']
			return_msg = send_email(email,'forget')
			if return_msg == '':
				context['title'] = '邮件已发送,请查收^_^'
				return render(request,'user/send_response.html',context)
			elif return_msg == '邮箱地址错误':
				context['title'] = '邮箱地址错误,请检查您的邮箱是否输入错误'
				return render(request,'user/send_response.html',context)
			else:
				context['title'] = '网络连接失败，请检查您的网络连接'
				return render(request,'user/send_response.html',context)
		else:
			context['forget_form'] = forget_form
			return render(request,'user/forgetpwd.html',context)

class ResetView(View):

	def get(self,request,active_code):
		context = {}
		all_records = EmailVerifyRecord.objects.filter(code=active_code)
		if all_records:
			record = all_records.order_by('-send_time')[0]
			email = record.email
			context['email'] = email
			return render(request,'user/password_reset.html',context)
		else:
			return render(request,'user/active_fail.html',context)

class ModifyPasswordView(View):

	def post(self,request):
		context = {}
		modify_form = ModifyPasswordForm(request.POST)

		if modify_form.is_valid():
			email = request.POST.get('email')
			new_password = modify_form.cleaned_data['password2']
			user = UserProfile.objects.get(email=email)
			user.set_password(new_password)
			user.save()
			#删除修改密码时发送验证码记录
			for record in EmailVerifyRecord.objects.filter(email=email,send_type='forget'):
				record.delete()

			return redirect('login')
		else:
			context['modify_form'] = modify_form
			return render(request,'user/password_reset.html',context)

class UserCenterInfoView(LoginRequiredMixin,View):

	def get(self,request):
		context = {}
		context['user'] = request.user

		return render(request,'user/usercenter-info.html',context)

	def post(self,request):
		response_data = {}
		userinfo_form = UserInfoForm(request.POST,instance=request.user)

		if userinfo_form.is_valid():
			userinfo_form.save()
			response_data['status'] = 'success'
			return JsonResponse(response_data)
		else:
			return JsonResponse(userinfo_form.errors)		

class UserAvaterUploadView(LoginRequiredMixin,View):

	def post(self,request):
		#声明instance实例来确定对哪个对象进行修改
		avater_form = ModifyUserAvaterForm(request.POST,request.FILES,instance=request.user)
		response_data = {}

		if avater_form.is_valid():
			avater_form.save()
			response_data['status'] = 'success'
			return JsonResponse(response_data)

		response_data['status'] = 'fail'

		return JsonResponse(response_data)

class UpdatePasswordView(LoginRequiredMixin,View):
	"""
	在个人中心里面修改密码
	"""
	def post(self,request):
		response_data = {}
		update_form = ModifyPasswordForm(request.POST)

		if update_form.is_valid():
			new_password = update_form.cleaned_data['password2']
			user = request.user
			user.set_password(new_password)
			user.save()
			response_data['status'] = 'success'

			return JsonResponse(response_data)
		else:
			return JsonResponse(update_form.errors)

class SendVerifyCodeView(View):
	"""
	在个人中心页面发送邮箱验证码
	"""
	def get(self,request):
		email = request.GET.get('email','')
		response_data = {}

		if not email:
			response_data['status'] = 'fail'
			response_data['msg'] = '邮箱不能为空'
			return JsonResponse(response_data)

		if UserProfile.objects.filter(email=email):
			response_data['status'] = 'fail'
			response_data['msg'] = '此邮箱已被注册'
			return JsonResponse(response_data)

		return_msg = send_email(email,'modify')
		if return_msg == '':
			response_data['status'] = 'success'
		elif return_msg == '邮箱地址错误':
			response_data['status'] = 'fail'
			response_data['msg'] = '邮箱地址错误'
		else:
			response_data['status'] = 'fail'
			response_data['msg'] = '网络连接失败'

		return JsonResponse(response_data)

class ModifyEmailView(LoginRequiredMixin,View):
	"""
	在个人中心修改邮箱
	"""
	def post(self,request):
		email = request.POST.get('email','')
		code = request.POST.get('code','')
		response_data = {}

		if email == '':
			response_data['status'] = 'fail'
			response_data['msg'] = '邮箱不能为空'
			return JsonResponse(response_data)

		if code == '':
			response_data['status'] = 'fail'
			response_data['msg'] = '验证码不能为空'
			return JsonResponse(response_data)

		existed_record = EmailVerifyRecord.objects.filter(email=email,code=code)

		if existed_record:
			user = request.user
			user.email = email
			user.save()
			#删除在个人中心修改邮箱时发送的验证码记录
			for record in EmailVerifyRecord.objects.filter(email=email,send_type='modify'):
				record.delete()
			response_data['status'] = 'success'
		else:
			response_data['status'] = 'fail'
			response_data['msg'] = '验证码错误'

		return JsonResponse(response_data)


class SendMobileCodeView(LoginRequiredMixin,View):
	"""
	在个人中心页面发送手机验证码
	"""
	def post(self,request):
		mobile = request.POST.get('mobile','')
		response_data = {}
		#验证mobile合法性
		if mobile == '':
			response_data['status'] = 'fail'
			response_data['msg'] = '手机号码不能为空'
			return JsonResponse(response_data)

		if not re.match(REGEX_MOBILE,mobile):
			response_data['status'] = 'fail'
			response_data['msg'] = '手机号码非法'
			return JsonResponse(response_data)

		if UserProfile.objects.filter(mobile=mobile):
			response_data['status'] = 'fail'
			response_data['msg'] = '此号码已被注册'
			return JsonResponse(response_data)

		code = '%04d' % random.randint(0,9999)
		#将验证码保存
		record = MobileVerifyRecord()
		record.mobile = mobile
		record.code = str(code)
		record.save()

		#发送短信验证码
		try:
			ccp.sendTemplateSMS(mobile,[str(code),SMS_CODE_EXPIRES_SECONDS/60],1)
			response_data['status'] = 'success'
		except Exception:
			response_data['status'] = 'fail'
			response_data['msg'] = '验证码发送失败'
		
		return JsonResponse(response_data)

class ModifyMobileView(LoginRequiredMixin,View):
	"""
	在个人中心修改手机号码
	"""
	def post(self,request):
		mobile = request.POST.get('mobile','')
		code = request.POST.get('code','')
		response_data = {}

		if mobile == '':
			response_data['status'] = 'fail'
			response_data['msg'] = '手机号码不能为空'
			return JsonResponse(response_data)

		if not re.match(REGEX_MOBILE,mobile):
			response_data['status'] = 'fail'
			response_data['msg'] = '手机号码非法'
			return JsonResponse(response_data)

		if UserProfile.objects.filter(mobile=mobile):
			response_data['status'] = 'fail'
			response_data['msg'] = '此号码已被注册'
			return JsonResponse(response_data)

		if code == '':
			response_data['status'] = 'fail'
			response_data['msg'] = '验证码不能为空'
			return JsonResponse(response_data)

		all_records = MobileVerifyRecord.objects.filter(mobile=mobile,code=code)

		if not all_records:
			response_data['status'] = 'fail'
			response_data['msg'] = '验证码错误'
		else:
			user = request.user
			user.mobile = mobile
			user.save()
			response_data['status'] = 'success'

		return JsonResponse(response_data)

class MyCourseView(LoginRequiredMixin,View):

	def get(self,request):
		context = {}
		context['user_courses'] = UserCourse.objects.filter(user=request.user)

		return render(request,'user/usercenter-mycourse.html',context)

class MyFavOrgView(LoginRequiredMixin,View):

	def get(self,request):
		context = {}
		org_list = []
		userfavs = UserFav.objects.filter(user=request.user,fav_type=2)
		for userfav in userfavs:
			org_list.append(CourseOrganization.objects.get(id=userfav.fav_id))

		context['org_list'] = org_list

		return render(request,'user/usercenter-fav-org.html',context)

class MyFavTeacherView(LoginRequiredMixin,View):

	def get(self,request):
		context = {}
		teacher_list = []
		userfavs = UserFav.objects.filter(user=request.user,fav_type=3)
		for userfav in userfavs:
			teacher_list.append(Teacher.objects.get(id=userfav.fav_id))

		context['teacher_list'] = teacher_list

		return render(request,'user/usercenter-fav-teacher.html',context)

class MyFavCourse(LoginRequiredMixin,View):

	def get(self,request):
		context = {}
		course_list = []
		userfavs = UserFav.objects.filter(user=request.user,fav_type=1)
		for userfav in userfavs:
			course_list.append(Course.objects.get(id=userfav.fav_id))

		context['course_list'] = course_list

		return render(request,'user/usercenter-fav-course.html',context)

class MyMessageView(LoginRequiredMixin,View):

	def get(self,request):
		context = {}
		all_messages = UserMessage.objects.filter(user=request.user.id)
		all_unread_messages = UserMessage.objects.filter(user=request.user.id,has_read=False)
		#进入个人中心的消息页面后所有未读消息置为True
		for unread_message in all_unread_messages:
			unread_message.has_read = True
			unread_message.save()

		#分页
		try:
			page = request.GET.get('page',1)
		except PageNotAnInteger:
			page = 1

		p = Paginator(all_messages,5,request=request)

		messages = p.page(page)

		context['messages'] = messages

		return render(request,'user/usercenter-message.html',context)

class MyOrderView(LoginRequiredMixin,View):
	"""
	个人中心我的订单页面
	"""
	def get(self,request):
		context = {}
		all_orders = Order.objects.filter(user_id=request.user.id)
		#分页
		try:
			page = request.GET.get('page',1)
		except PageNotAnInteger:
			page = 1

		p = Paginator(all_orders,5,request=request)

		my_orders = p.page(page)

		context['my_orders'] = my_orders

		return render(request,'user/usercenter-myorders.html',context)







