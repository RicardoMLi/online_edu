from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField

#城市model
class CityDict(models.Model):
	name = models.CharField(max_length=50,verbose_name='城市名称')
	desc = models.CharField(max_length=200,verbose_name='城市描述')
	created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

	class Meta:
		verbose_name = '城市信息'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name


#课程机构model
class CourseOrganization(models.Model):
	name = models.CharField(max_length=50,verbose_name='机构名称')
	category = models.CharField(max_length=20,choices=(('organization','培训机构'),('college','大学'),('personal','个人')),default='organization',verbose_name='机构类别')
	desc = RichTextUploadingField(verbose_name='机构描述')
	tag = models.CharField(default='全国知名',max_length=20,verbose_name='机构标签')
	slogan = models.CharField(max_length=100,default='你旺,我旺,大家旺',verbose_name='标语')
	click_num = models.IntegerField(default=0,verbose_name='点击量')
	fav_num = models.IntegerField(default=0,verbose_name='收藏人数')
	address = models.CharField(max_length=100,default='',verbose_name='机构地址')
	students_num = models.IntegerField(default=0,verbose_name='学习人数')
	course_num = models.IntegerField(default=0,verbose_name='课程数量')
	image = models.ImageField(upload_to='organization/%Y/%m',null=True,blank=True,max_length=100,verbose_name='机构封面图')
	city = models.ForeignKey(CityDict,verbose_name='机构所在城市',on_delete=models.DO_NOTHING)
	created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

	#获取本机构经典课程
	def get_courses(self):
		return self.course_set.all().order_by('-click_num')[:2]

	#获取本机构课程数量
	def get_course_nums(self):
		return self.course_set.all().count()

	#获取讲师数量
	def get_teacher_nums(self):
		return self.teacher_set.all().count()

	#获取机构学习人数
	def get_student_nums(self):
		total = 0
		for course in self.course_set.all():
			total += course.students_num
		return total

	class Meta:
		verbose_name = '授课机构信息'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name


#讲师model
class Teacher(models.Model):
	organization = models.ForeignKey(CourseOrganization,on_delete=models.DO_NOTHING,verbose_name='入职机构')
	name = models.CharField(max_length=20,verbose_name='教师名称')
	work_years = models.IntegerField(default=0,verbose_name='工作年限')
	age = models.IntegerField(default=18,verbose_name='年龄')
	teaching_trait = models.CharField(default='',max_length=200,verbose_name='教学特点')
	work_company = models.CharField(max_length=50,verbose_name='就职公司')
	work_position = models.CharField(max_length=50,verbose_name='职位')
	click_num = models.IntegerField(default=0,verbose_name='点击量')
	fav_num = models.IntegerField(default=0,verbose_name='收藏人数')
	avater = models.ImageField(upload_to='teacher/%Y/%m',default='',null=True,blank=True,verbose_name='讲师头像')
	created_time = models.DateTimeField(auto_now_add=True,verbose_name='入职时间')

	def get_course_nums(self):
		return self.course_set.all().count()

	#获取讲师最经典课程
	def get_wonderful_course(self):
		return self.course_set.all().order_by('-fav_num')[0] if self.course_set.all() else None

	class Meta:
		verbose_name = '授课机构讲师信息'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name




