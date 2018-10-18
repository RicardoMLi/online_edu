from django.urls import path

from .views import UserAskView,UserFavView,CommentView

urlpatterns = [
	path('userask/',UserAskView.as_view(),name='userask'),
	path('userfav/',UserFavView.as_view(),name='userfav'),
	path('add_comment/',CommentView.as_view(),name='add_comment'),
]