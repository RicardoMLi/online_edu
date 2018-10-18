from django.urls import path

from .views import CourseListView,CourseDetailView,CourseInfoView,CourseCommentView,VideoPlayView

urlpatterns = [
	path('course_list/',CourseListView.as_view(),name='course_list'),
	path('course_detail/<int:course_id>',CourseDetailView.as_view(),name='course_detail'),
	path('course_info/<int:course_id>',CourseInfoView.as_view(),name='course_info'),
	path('course_comment/<int:course_id>',CourseCommentView.as_view(),name='course_comment'),
	path('video_play/<int:video_id>',VideoPlayView.as_view(),name='video_play'),
]