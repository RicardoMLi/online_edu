from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField
from organization.models import CourseOrganization,Teacher

class Course(models.Model):
	course_org = models.ForeignKey(CourseOrganization,on_delete=models.DO_NOTHING,verbose_name='所属课程机构',null=True,blank=True)
	name = models.CharField(max_length=50,verbose_name='课程名称')
	teacher = models.ForeignKey(Teacher,null=True,blank=True,on_delete=models.DO_NOTHING,verbose_name='讲师')
	short_desc = models.CharField(max_length=300,verbose_name='课程简述')
	detail_desc = RichTextUploadingField(verbose_name='课程描述')
	degree = models.CharField(choices=(('primary','初级'),('junior','中级'),('senior','高级')),max_length=10,verbose_name='难易程度')
	study_duration = models.IntegerField(default=0,verbose_name='学习时长')
	students_num = models.IntegerField(default=0,verbose_name='学习人数')
	fav_num = models.IntegerField(default=0,verbose_name='收藏人数')
	click_num = models.IntegerField(default=0,verbose_name='点击量')
	is_free = models.BooleanField(default=True,verbose_name='是否免费')
	price = models.FloatField(default=0,verbose_name='课程价格')
	category = models.CharField(default='后端开发',max_length=40,verbose_name='课程类别')
	tag = models.CharField(default='',max_length=20,verbose_name='课程标签')
	is_banner = models.BooleanField(default=False,verbose_name='首页轮播')
	you_need_know = models.CharField(max_length=300,default='',null=True,blank=True,verbose_name='课程须知')
	you_can_get = models.CharField(max_length=300,default='',null=True,blank=True,verbose_name='课程收获')
	image = models.ImageField(upload_to='course/%Y/%m',null=True,blank=True,verbose_name='课程封面图',max_length=100)
	created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

	#根据name去重
	def __eq__(self,other):
		if isinstance(other,Course):
			return self.name == other.name
		else:
			return False

	def __ne__(self,other):
		return (not self.__eq__(other))

	#获取课程章节数量
	def get_chapter_nums(self):
		return self.chapter_set.all().count()

	get_chapter_nums.short_description = '章节数'

	#获取所有章节
	def get_all_chapters(self):
		return self.chapter_set.all()

	#获取学习用户
	def get_student_users(self):
		return self.usercourse_set.all()

	class Meta:
		verbose_name = '课程信息'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name

class BannerCourse(Course):

	class Meta:
		verbose_name = '轮播课程'
		verbose_name_plural = verbose_name
		proxy = True


#课程章节model
class Chapter(models.Model):
	course = models.ForeignKey(Course,on_delete=models.CASCADE,verbose_name='课程')
	name = models.CharField(max_length=100,verbose_name='章节名称')
	created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

	#获取章节视频
	def get_chapter_video(self):
		return self.video_set.all()

	class Meta:
		verbose_name = '课程章节'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name


#课程视频model
class Video(models.Model):
	chapter = models.ForeignKey(Chapter,on_delete=models.CASCADE,verbose_name='章节')
	name = models.CharField(max_length=100,verbose_name='视频名称')
	url = models.CharField(max_length=100,default='',verbose_name='视频链接')
	created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

	class Meta:
		verbose_name = '课程视频'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name


class CourseResource(models.Model):
	course = models.ForeignKey(Course,on_delete=models.CASCADE,verbose_name='课程')
	name = models.CharField(max_length=50,verbose_name='资源名称')
	download_path = models.FileField(upload_to='course/resource/%Y/%m',verbose_name='资源下载地址')
	created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

	class Meta:
		verbose_name = '课程资源'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name