from django.db import models


from user.models import UserProfile
from course.models import Course


#用户咨询model
class UserAsk(models.Model):
	name = models.CharField(max_length=20,verbose_name='用户名')
	mobile = models.CharField(max_length=11,verbose_name='手机号码')
	course_name = models.CharField(max_length=50,verbose_name='课程名称')
	created_time = models.DateTimeField(auto_now_add=True,verbose_name='询问时间')

	class Meta:
		verbose_name = '用户咨询'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name


#课程评论model
class CourseComment(models.Model):
	user = models.ForeignKey(UserProfile,on_delete=models.DO_NOTHING,verbose_name='用户名')
	course = models.ForeignKey(Course,on_delete=models.DO_NOTHING,verbose_name='课程名')
	comment = models.CharField(max_length=200,verbose_name='评论')
	created_time = models.DateTimeField(auto_now_add=True,verbose_name='评论时间')

	class Meta:
		verbose_name = '课程评论'
		verbose_name_plural = verbose_name

	def __str__(self):
		return '%s -> %s' % (self.user.username,self.course.name) 


#用户收藏model
class UserFav(models.Model):
	user = models.ForeignKey(UserProfile,on_delete=models.DO_NOTHING,verbose_name='用户名')
	#通过下面两个字段来处理用户收藏的是课程、机构还是讲师
	fav_id = models.IntegerField(default=0,verbose_name='数据id')
	fav_type = models.IntegerField(choices=((1,'课程'),(2,'机构'),(3,'讲师')),default=1,verbose_name='收藏类型')

	created_time = models.DateTimeField(auto_now_add=True,verbose_name='收藏时间')

	class Meta:
		verbose_name = '用户收藏'
		verbose_name_plural = verbose_name

	def __str__(self):
		return '%s -> %d' % (self.user.username,self.fav_type) 


#消息model
class UserMessage(models.Model):
	#默认为0，为所有用户发送该消息
	user = models.IntegerField(default=0,verbose_name='接收用户')
	message = models.CharField(max_length=500,verbose_name='消息内容')
	has_read = models.BooleanField(default=False,verbose_name='是否已读')
	created_time = models.DateTimeField(auto_now_add=True,verbose_name='发送时间')

	class Meta:
		verbose_name = '用户消息'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.message


#用户课程model
class UserCourse(models.Model):
	user = models.ForeignKey(UserProfile,on_delete=models.DO_NOTHING,verbose_name='用户名')
	course = models.ForeignKey(Course,on_delete=models.DO_NOTHING,verbose_name='课程名')
	created_time = models.DateTimeField(auto_now_add=True,verbose_name='开始学习时间')

	class Meta:
		verbose_name = '用户课程'
		verbose_name_plural = verbose_name

	def __str__(self):
		return '%s -> %s' % (self.user.username,self.course.name)





