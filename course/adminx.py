import xadmin

from .models import Course,Chapter,Video,CourseResource,BannerCourse

class ChapterInline(object):
	model = Chapter
	extra = 0

class VideoInline(object):
	model = Video
	extra = 0

class CourseResourceInline(object):
	model = CourseResource
	extra = 0

class CourseAdmin(object):
	list_display = ['name','short_desc','degree','get_chapter_nums','study_duration','students_num','fav_num','click_num','image','created_time']
	search_fields = ['name','short_desc','degree','study_duration','students_num','fav_num','click_num','image']
	list_filter = ['name','short_desc','degree','study_duration','students_num','fav_num','click_num','image','created_time']
	inlines = [ChapterInline,CourseResourceInline]

	#在保存课程的时候统计课程机构的课程数
	def save_models(self):
		obj = self.new_obj
		obj.save()

		if obj.course_org:
			course_org = obj.course_org
			course_org.course_num = Course.objects.filter(course_org=course_org).count()
			course_org.save()

class BannerCourseAdmin(object):
	list_display = ['name','short_desc','degree','get_chapter_nums','study_duration','students_num','fav_num','click_num','image','created_time']
	search_fields = ['name','short_desc','degree','study_duration','students_num','fav_num','click_num','image']
	list_filter = ['name','short_desc','degree','study_duration','students_num','fav_num','click_num','image','created_time']
	inlines = [ChapterInline,CourseResourceInline]

	def queryset(self):
		qs = super(BannerCourseAdmin,self).queryset()
		return qs.filter(is_banner=True)

class ChapterAdmin(object):
	list_display = ['course','name','created_time']
	search_fields = ['course__name','name']
	list_filter = ['course__name','name','created_time']
	inlines = [VideoInline]

class VideoAdmin(object):
	list_display = ['chapter','name','created_time']
	search_fields = ['chapter__name','name']
	list_filter = ['chapter__name','name','created_time']

class CourseResourceAdmin(object):
	list_display = ['course','name','download_path','created_time']
	search_fields = ['course__name','name','download_path']
	list_filter = ['course__name','name','download_path','created_time']


xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(BannerCourse,BannerCourseAdmin)
xadmin.site.register(Chapter,ChapterAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)