import random
import time

from datetime import datetime
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.generic.base import View

from .models import Order
from course.models import Course
from user.models import UserProfile
from Mxonline.settings import APP_PRIVATE_KEY_PATH,ALI_PUBLIC_KEY_PATH,APP_ID,RETURN_URL
from utils.mixin_utils import LoginRequiredMixin
from utils.alipay import AliPay

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

class DealOrderView(View):
	"""
	订单确认
	"""
	def get(self,request):
		user_id = request.GET.get('user_id','')
		course_id = request.GET.get('course_id','')
		response_data = {}

		if user_id == '' or course_id == '':
			response_data['status'] = 'fail'
			response_data['msg'] = '用户id或课程id不能为空'
			return JsonResponse(response_data)

		user_id = int(user_id)
		course_id = int(course_id)

		if not (Course.objects.filter(id=course_id).exists() and UserProfile.objects.filter(id=user_id).exists()):
			response_data['status'] = 'fail'
			response_data['msg'] = '用户或课程未找到'
			return JsonResponse(response_data)

		user = UserProfile.objects.get(id=user_id)
		course = Course.objects.get(id=course_id)
		#生成订单编号
		order_code = '{time_str}{user_id}{rand_int}'.format(time_str=time.strftime('%Y%m%d%H%M%S'),user_id=user.id,rand_int=random.Random().randint(10,99))
		#生成订单
		order = Order()
		order.user = user
		order.course = course
		order.order_code = order_code
		order.order_amount = course.price
		order.save()

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
			response = redirect('user_info')
		else:
			response = redirect('index')
		
		return response



