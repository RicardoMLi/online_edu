from django.urls import path

from .views import AddShoppingCartView,DeleteShoppingCartView,CheckShoppingCartView,OrderInfoView,DealOrderView,AlipayView,OrderDetailView

urlpatterns = [
	path('add_shoppingcart/',AddShoppingCartView.as_view(),name='add_shoppingcart'),
	path('delete/',DeleteShoppingCartView.as_view(),name='delete'),
	path('check_course/',CheckShoppingCartView.as_view(),name='check_course'),
	path('order_info/<str:user_id>',OrderInfoView.as_view(),name='order_info'),
	path('deal_order/',DealOrderView.as_view(),name='deal_order'),
	path('alipay_return/',AlipayView.as_view(),name='alipay_return'),
	path('order_detail/<int:order_code>',OrderDetailView.as_view(),name='order_detail'),
]