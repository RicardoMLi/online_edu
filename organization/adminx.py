import xadmin

from .models import CityDict,CourseOrganization,Teacher


class CityDictAdmin(object):
	list_display = ['name','desc','created_time']
	search_fields = ['name','desc']
	list_filter = ['name','desc','created_time']

class CourseOrganizationAdmin(object):
	list_display = ['name','category','desc','click_num','fav_num','address','image','city','created_time']
	search_fields = ['name','category','desc','click_num','fav_num','address','image','city__name']
	list_filter = ['name','category','desc','click_num','fav_num','address','image','city__name','created_time']
	relfield_style = 'fk-ajax'

class TeacherAdmin(object):
	list_display = ['organization','name','work_years','work_company','work_position','click_num','fav_num','created_time']
	search_fields = ['organization','name','work_years','work_company','work_position','click_num','fav_num']
	list_filter = ['organization__name','name','work_years','work_company','work_position','click_num','fav_num','created_time']


xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(CourseOrganization,CourseOrganizationAdmin)
xadmin.site.register(Teacher,TeacherAdmin)
