from django.urls import path

from .views import OrderInfoView,DealOrderView,AlipayView

urlpatterns = [
	path('order_info/<str:info>',OrderInfoView.as_view(),name='order_info'),
	path('deal_order/',DealOrderView.as_view(),name='deal_order'),
	path('alipay_return/',AlipayView.as_view(),name='alipay_return'),
]