import xadmin

from .models import UserAsk,CourseComment,UserFav,UserMessage,UserCourse


class UserAskAdmin(object):
	list_display = ['name','mobile','course_name','created_time']
	search_fields = ['name','mobile','course_name']
	list_filter = ['name','mobile','course_name','created_time']

class CourseCommentAdmin(object):
	list_display = ['user','course','comment','created_time']
	search_fields = ['user__username','course__name','comment']
	list_filter =  ['user__username','course__name','comment','created_time']

class UserFavAdmin(object):
	list_display = ['user','fav_id','fav_type','created_time']
	search_fields = ['user__username','fav_id','fav_type']
	list_filter = ['user__username','fav_id','fav_type','created_time']

class UserMessageAdmin(object):
	list_display = ['user','message','has_read','created_time']
	search_fields = ['user','message','has_read']
	list_filter = ['user','message','has_read','created_time']

class UserCourseAdmin(object):
	list_display = ['user','course','created_time']
	search_fields = ['user__username','course__name']
	list_filter = ['user__username','course__name','created_time']


xadmin.site.register(UserAsk,UserAskAdmin)
xadmin.site.register(CourseComment,CourseCommentAdmin)
xadmin.site.register(UserFav,UserFavAdmin)
xadmin.site.register(UserMessage,UserMessageAdmin)
xadmin.site.register(UserCourse,UserCourseAdmin)
