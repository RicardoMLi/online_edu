from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
	nickname = models.CharField(max_length=50,verbose_name='昵称',default='')
	gender = models.CharField(max_length=6,choices=(('male','男'),('female','女')),null=True,blank=True,verbose_name='性别')
	birthday = models.DateField(null=True,blank=True,verbose_name='生日')
	mobile = models.CharField(max_length=11,null=True,blank=True,verbose_name='电话')
	address = models.CharField(max_length=100,default='',null=True,blank=True,verbose_name='地址')
	#默认False,在激活账号后改为True,以此区分第三方登录创建账号和邮箱创建账号
	not_third = models.BooleanField(default=False,verbose_name='不是第三方登录创建')
	avater = models.ImageField(upload_to='images/%Y/%m',default='image/default.png',null=True,blank=True,max_length=100)

	#获取用户未读消息数量
	def get_unreadmessage_num(self):
		from user_operation.models import UserMessage
		return UserMessage.objects.filter(user=self.id,has_read=False).count()

	class Meta:
		verbose_name = '用户信息'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.username


class EmailVerifyRecord(models.Model):
	code = models.CharField(max_length=20,verbose_name='验证码')
	email = models.EmailField(max_length=50,verbose_name='邮箱')
	#注册和找回密码均要使用验证码
	send_type = models.CharField(choices=(('register','注册'),('forget','找回密码'),('modify','修改邮箱')),max_length=10,verbose_name='验证码类型')
	send_time = models.DateTimeField(auto_now_add=True,verbose_name='发送时间')

	class Meta:
		verbose_name = '邮箱验证码'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.code

class MobileVerifyRecord(models.Model):
	code = models.CharField(max_length=4,verbose_name='验证码')
	mobile = models.CharField(max_length=11,verbose_name='手机号码')
	send_time = models.DateTimeField(auto_now_add=True,verbose_name='发送时间')

	class Meta:
		verbose_name = '短信验证码'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.code 

class Banner(models.Model):
	title = models.CharField(max_length=100,verbose_name='标题')
	image = models.ImageField(upload_to='banner/%Y/%m',null=True,blank=True,verbose_name='轮播图')
	index = models.IntegerField(verbose_name='轮播顺序')
	created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间') 

	class Meta:
		verbose_name = '轮播图'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.title