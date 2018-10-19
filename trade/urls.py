from django.urls import path

from .views import OrderInfoView

urlpatterns = [
	path('order_info/<str:info>',OrderInfoView.as_view(),name='order_info'),
]