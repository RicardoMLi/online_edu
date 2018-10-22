import random
import time

from datetime import datetime
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.db.models import Q
from django.views.generic.base import View

from .models import Order,ShoppingCart,CourseInOrder
from course.models import Course
from user.models import UserProfile
from Mxonline.settings import APP_PRIVATE_KEY_PATH,ALI_PUBLIC_KEY_PATH,APP_ID,RETURN_URL
from utils.mixin_utils import LoginRequiredMixin
from utils.alipay import AliPay

class AddShoppingCartView(View):
	"""
	加入购物车
	"""
	def post(self,request):
		user_id = request.POST.get('user_id','')
		course_id = request.POST.get('course_id','')
		response_data = {}

		if user_id == '' or course_id == '':
			response_data['status'] = 'fail'
			response_data['msg'] = '用户id或课程id不能为空'
			return JsonResponse(response_data)

		try:
			user_id = int(user_id)
			course_id = int(course_id)
		except ValueError:
			response_data['status'] = 'fail'
			response_data['msg'] = '用户id或课程id错误'
			return JsonResponse(response_data)

		if not (Course.objects.filter(id=course_id).exists() and UserProfile.objects.filter(id=user_id).exists()):
			response_data['status'] = 'fail'
			response_data['msg'] = '用户或课程不存在'
			return JsonResponse(response_data)

		if ShoppingCart.objects.filter(user_id=user_id,course_id=course_id).exists():
			response_data['status'] = 'fail'
			response_data['msg'] = '您已将本课程加入购物车'
			return JsonResponse(response_data)

		order = Order.objects.filter(user_id=user_id,pay_status='TRADE_SUCCESS')
		if order:
			coursesInOrder = [couseInOrder.course for couseInOrder in CourseInOrder.objects.filter(order_id=order[0].id)]
			if Course.objects.get(id=course_id) in coursesInOrder:
				response_data['status'] = 'fail'
				response_data['msg'] = '您已购买本课程,无须重复购买'
				return JsonResponse(response_data)

		cart = ShoppingCart()
		cart.user = UserProfile.objects.get(id=user_id)
		cart.course = Course.objects.get(id=course_id)
		cart.save()
		response_data['status'] = 'success'
		response_data['msg'] = '加入购物车成功'

		return JsonResponse(response_data)

class DeleteShoppingCartView(LoginRequiredMixin,View):
	"""
	删除购物车某件商品
	"""
	def post(self,request):
		user_id = request.POST.get('user_id','')
		course_id = request.POST.get('course_id','')
		response_data = {}
		if course_id == '' or user_id == '':
			response_data['status'] = 'fail'
			response_data['msg'] = '用户id或课程id不能为空'
			return JsonResponse(response_data)

		try:
			user_id = int(user_id)
			course_id = int(course_id)
		except ValueError:
			response_data['status'] = 'fail'
			response_data['msg'] = '用户id或课程id错误'
			return JsonResponse(response_data)

		record = ShoppingCart.objects.filter(user_id=user_id,course_id=course_id)
		#记录不存在
		if not record:
			response_data['status'] = 'fail'
			response_data['msg'] = '商品不存在购物车内'
			return JsonResponse(response_data)

		record[0].delete()
		response_data['status'] = 'success'
		response_data['msg'] = '删除成功'
		return JsonResponse(response_data)

class CheckShoppingCartView(LoginRequiredMixin,View):
	"""
	检测用户是否将本课程加入购物车
	"""
	def post(self,request):
		response_data = {}
		user_id = request.POST.get('user_id','')
		course_id = request.POST.get('course_id','')

		code = ((1,'课程免费'),(2,'加入购物车但未支付'),(3,'出现错误'),(4,'支付成功'),(5,'加入购物车'))

		if user_id == '' or course_id == '':
			response_data['status'] = 'fail'
			response_data['msg'] = code[2][0]
			return JsonResponse(response_data)

		try:
			user_id = int(user_id)
			course_id = int(course_id)
		except ValueError:
			response_data['status'] = 'fail'
			response_data['msg'] = code[2][0]
			return JsonResponse(response_data)

		if user_id != request.user.id:
			response_data['status'] = 'fail'
			response_data['msg'] = code[2][0]
			return JsonResponse(response_data)

		#本课程免费
		if Course.objects.filter(id=course_id,is_free=True):
			response_data['status'] = 'success'
			response_data['msg'] = code[0][0]
		else:
			#用户已将本课程加入购物车
			if ShoppingCart.objects.filter(user_id=user_id,course_id=course_id).exists():			
				response_data['status'] = 'success'
				response_data['msg'] = code[1][0]
			else:
				#判断用户是否已结算
				order = Order.objects.filter(user_id=user_id,pay_status='TRADE_SUCCESS')
				if order:
					coursesInOrder = [couseInOrder.course for couseInOrder in CourseInOrder.objects.filter(order_id=order[0].id)]
					if Course.objects.get(id=course_id) in coursesInOrder:
						response_data['status'] = 'success'
						response_data['msg'] = code[3][0]
					else:
						response_data['status'] = 'fail'
						response_data['msg'] = code[4][0]	
				else:
					response_data['status'] = 'fail'
					response_data['msg'] = code[4][0]			

		return JsonResponse(response_data)
		
class OrderInfoView(LoginRequiredMixin,View):

	def get(self,request,user_id):
		context = {}
		if user_id == '':
			return render(request,'404.html',context)

		user_id = int(user_id)

		if not UserProfile.objects.filter(id=user_id).exists():
			return render(request,'404.html',context)
		
		course_list = []
		#加入购物车内商品
		carts = ShoppingCart.objects.filter(user_id=user_id)
		if carts:
			for cart in carts:
				course_list.append(cart.course)

		#可能用户有未支付的订单商品
		unpaidorder_list = Order.objects.filter(Q(user_id=request.user.id)&(~Q(pay_status='TRADE_SUCCESS')))
		#加入未支付订单内商品
		if unpaidorder_list:
			coursesorder_list = [CourseInOrder.objects.get(order_id=order.id) for order in unpaidorder_list]
			for courseorder in coursesorder_list:
				course_list.append(courseorder.course)

		context['course_list'] = course_list
		return render(request,'trade/order.html',context)

class DealOrderView(LoginRequiredMixin,View):
	"""
	订单确认
	"""
	def post(self,request):
		user_id = request.POST.get('user_id','')
		response_data = {}

		if user_id == '':
			response_data['status'] = 'fail'
			response_data['msg'] = '用户id不能为空'
			return JsonResponse(response_data)
		try:
			user_id = int(user_id)
		except ValueError:
			response_data['status'] = 'fail'
			response_data['msg'] = '用户错误'
			return JsonResponse(response_data)		

		if not UserProfile.objects.filter(id=user_id).exists():
			response_data['status'] = 'fail'
			response_data['msg'] = '用户不存在'
			return JsonResponse(response_data)

		user = UserProfile.objects.get(id=user_id)
		#将购物车内的商品删除
		order_amount = 0
		for cart in ShoppingCart.objects.filter(user_id=user_id):
			order_amount += cart.course.price

		#加入未支付订单内商品
		unpaidorder_list = Order.objects.filter(Q(user_id=request.user.id)&(~Q(pay_status='TRADE_SUCCESS')))
		if unpaidorder_list:
			coursesorder_list = [CourseInOrder.objects.get(order_id=order.id) for order in unpaidorder_list]
			for courseorder in coursesorder_list:
				order_amount += courseorder.course.price

		#生成订单编号
		order_code = '{time_str}{user_id}{rand_int}'.format(time_str=time.strftime('%Y%m%d%H%M%S'),user_id=user.id,rand_int=random.Random().randint(10,99))
		#生成订单
		order = Order()
		order.user = user
		order.order_code = order_code
		order.order_amount = order_amount
		order.save()

		for cart in ShoppingCart.objects.filter(user_id=user_id):
			#将课程与订单关联
			orderCourse =  CourseInOrder()
			orderCourse.order = order
			orderCourse.course = cart.course
			orderCourse.save()
			cart.delete()

		#将未支付订单删除并且将重新关联课程与订单
		if unpaidorder_list:
			for unpaidorder in unpaidorder_list:
				coursesorder_list = [CourseInOrder.objects.get(order_id=order.id) for order in unpaidorder_list]
				for courseorder in coursesorder_list:
					#重新关联课程与订单
					orderCourse =  CourseInOrder()
					orderCourse.order = order
					orderCourse.course = courseorder.course
					orderCourse.save()
					#之前关联的课程与订单删除
					courseorder.delete()					
				#未支付订单删除
				unpaidorder.delete()

		#生成return_url
		alipay = AliPay(
            app_id=APP_ID,
            app_notify_url=RETURN_URL,
            app_private_key_path=APP_PRIVATE_KEY_PATH,
            alipay_public_key_path=ALI_PUBLIC_KEY_PATH,
            debug=True,
            return_url=RETURN_URL
        )

		url = alipay.direct_pay(
		    subject=order.order_code,
		    out_trade_no=order.order_code,
		    total_amount=order.order_amount
		)

		return_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

		response_data['status'] = 'success'
		response_data['return_url'] = return_url

		return JsonResponse(response_data)

class AlipayView(View):
	"""
	支付宝支付页面
	"""
	def get(self,request):
		processed_dict = {}
		for key, value in request.GET.items():
			processed_dict[key] = value

		sign = processed_dict.pop('sign', None)
		alipay = AliPay(
		    app_id=APP_ID,
		    app_notify_url=RETURN_URL,
		    app_private_key_path=APP_PRIVATE_KEY_PATH,
		    alipay_public_key_path=ALI_PUBLIC_KEY_PATH,
		    debug=True,
		    return_url=RETURN_URL
		)

		result_status = alipay.verify(processed_dict, sign)
		if result_status:
			order_code = processed_dict.get('out_trade_no', None)
			trade_no = processed_dict.get('trade_no', None)
			pay_status = processed_dict.get('trade_status') if processed_dict.get('trade_status') else 'TRADE_SUCCESS'
			
			existed_orders = Order.objects.filter(order_code=order_code)
			
			if existed_orders:
				existed_order = existed_orders[0]
				existed_order.pay_status = pay_status
				existed_order.trade_no = trade_no
				existed_order.paid_time = datetime.now()
				existed_order.save()
			response = redirect('myorders')
		else:
			response = redirect('index')
		
		return response

class OrderDetailView(LoginRequiredMixin,View):
	"""
	订单详情
	"""
	def get(self,request,order_code):
		context = {}
		record = Order.objects.filter(order_code=order_code)

		if not record:
			return render(request,'404.html',context)

		course_list = [courseorder.course for courseorder in CourseInOrder.objects.filter(order_id=record[0].id)]
		context['course_list'] = course_list

		return render(request,'trade/order-detail.html',context)




