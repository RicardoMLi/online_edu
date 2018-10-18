import xadmin
from xadmin import views

from .models import EmailVerifyRecord,Banner,MobileVerifyRecord

class BaseSetting(object):
	enable_themes = True
	use_bootswatch = True

class GlobalSettings(object):
	site_title = '慕学后台管理系统'
	site_footer = '慕学在线网'
	menu_style = 'accordion'

class EmailVerifyRecordAdmin(object):
	list_display = ['code','email','send_type','send_time']
	search_fields = ['code','email','send_type']
	list_filter = ['code','email','send_type','send_time']

class MobileVerifyRecordAdmin(object):
	list_display = ['code','mobile','send_time']
	search_fields = ['code','mobile']
	list_filter = ['code','mobile','send_time']

class BannerAdmin(object):
	list_display = ['title','image','index','created_time']
	search_fields = ['title','image','index']
	list_filter = ['title','image','index']


xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(MobileVerifyRecord,MobileVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)