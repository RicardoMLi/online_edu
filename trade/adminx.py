import xadmin

from .models import Order,ShoppingCart

class OrderAdmin(object):
	list_display = ['user','course','order_code','trade_no','pay_status','order_amount','paid_time','created_time']
	search_fields = ['user','course','order_code','trade_no','pay_status','order_amount']
	list_filter = ['user','course','order_code','trade_no','pay_status','order_amount','paid_time','created_time']

class ShoppingCartAdmin(object):
	list_display = ['user','course','created_time']
	search_fields = ['user','course']
	list_filter = ['user','course','created_time']


xadmin.site.register(Order,OrderAdmin)
xadmin.site.register(ShoppingCart,ShoppingCartAdmin)