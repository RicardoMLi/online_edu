import xadmin

from .models import Order,OrderCourse

class OrderAdmin(object):
	list_display = ['user','course','order_code','trade_no','pay_status','order_amount','paid_time','created_time']
	search_fields = ['user','course','order_code','trade_no','pay_status','order_amount']
	list_filter = ['user','course','order_code','trade_no','pay_status','order_amount','paid_time','created_time']

class OrderCourseAdmin(object):
	list_display = ['order','course']
	search_fields = ['order','course']
	list_filter = ['order','course']


xadmin.site.register(Order,OrderAdmin)
xadmin.site.register(OrderCourse,OrderCourseAdmin)