from django.urls import path

from .views import AddShoppingCartView,CheckShoppingCartView,OrderInfoView,DealOrderView,AlipayView

urlpatterns = [
	path('add_shoppingcart/',AddShoppingCartView.as_view(),name='add_shoppingcart'),
	path('check_course/',CheckShoppingCartView.as_view(),name='check_course'),
	path('order_info/<str:info>',OrderInfoView.as_view(),name='order_info'),
	path('deal_order/',DealOrderView.as_view(),name='deal_order'),
	path('alipay_return/',AlipayView.as_view(),name='alipay_return'),
]