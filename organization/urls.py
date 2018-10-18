from django.urls import path

from .views import OrganizationListView,OrganizationHomeView,OrganizationCourseView,OrganizationTeacherView,OrganizationDescriptionView,TeacherListView,TeacherDetailView

urlpatterns = [
	path('org_list/',OrganizationListView.as_view(),name='org_list'),
	path('org_home/<int:organization_id>',OrganizationHomeView.as_view(),name='org_home'),
	path('org_course/<int:organization_id>',OrganizationCourseView.as_view(),name='org_course'),
	path('org_teacher/<int:organization_id>',OrganizationTeacherView.as_view(),name='org_teacher'),
	path('org_desc/<int:organization_id>',OrganizationDescriptionView.as_view(),name='org_desc'),
	path('teacher_list',TeacherListView.as_view(),name='teacher_list'),
	path('teacher_detail/<int:teacher_id>',TeacherDetailView.as_view(),name='teacher_detail'),
]