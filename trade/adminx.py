import xadmin

from .models import Order,ShoppingCart,CourseInOrder

class OrderAdmin(object):
	list_display = ['user','order_code','trade_no','pay_status','order_amount','paid_time','created_time']
	search_fields = ['user','order_code','trade_no','pay_status','order_amount']
	list_filter = ['user','order_code','trade_no','pay_status','order_amount','paid_time','created_time']

class ShoppingCartAdmin(object):
	list_display = ['user','course','created_time']
	search_fields = ['user','course']
	list_filter = ['user','course','created_time']

class CourseInOrderAdmin(object):
	list_display = ['order','course',]
	search_fields = ['order','course']
	list_filter = ['order','course',]

xadmin.site.register(Order,OrderAdmin)
xadmin.site.register(ShoppingCart,ShoppingCartAdmin)
xadmin.site.register(CourseInOrder,CourseInOrderAdmin)