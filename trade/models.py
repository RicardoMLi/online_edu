from django.db import models

from user.models import UserProfile
from course.models import Course

class ShoppingCart(models.Model):
	user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,verbose_name='用户')
	course = models.ForeignKey(Course,on_delete=models.DO_NOTHING,verbose_name='课程')
	created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

	class Meta:
		verbose_name = '购物车'
		verbose_name_plural = verbose_name
		unique_together = ('user','course')

	def __str__(self):
		return '{username}-{course_name}'.format(username=self.user.username,course_name=self.course.name) 


class Order(models.Model):

	ORDER_STATUS = (
			('TRADE_CLOSED','交易关闭'),
			('TRADE_FINISHED','交易完结'),
			('TRADE_SUCCESS','支付成功'),
            ('WAIT_BUYER_PAY','交易创建'),
			('unpaid','待支付'),
		)

	user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,verbose_name='用户')
	order_code = models.CharField(max_length=30,unique=True,verbose_name='订单编号')
	trade_no = models.CharField(max_length=30,unique=True,null=True,blank=True,verbose_name='交易编号')
	pay_status = models.CharField(max_length=20,choices=ORDER_STATUS,default='unpaid',verbose_name='交易状态')
	order_amount = models.FloatField(verbose_name='订单金额')
	paid_time = models.DateTimeField(null=True,blank=True,verbose_name='支付时间')
	created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

	class Meta:
		verbose_name = '订单'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.order_code

#关联订单与订单内的课程
class CourseInOrder(models.Model):
	order = models.ForeignKey(Order,on_delete=models.CASCADE,verbose_name='订单')
	course = models.ForeignKey(Course,on_delete=models.DO_NOTHING,verbose_name='课程')

	class Meta:
		verbose_name = '订单课程'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.order.order_code
