from django.urls import path,include
from .views import LoginView,LogoutView,RegisterView,ActiveUserView,ForgetPasswordView,ResetView,ModifyPasswordView
from .views import UserCenterInfoView,UserAvaterUploadView,UpdatePasswordView,SendVerifyCodeView,ModifyEmailView
from .views import MyCourseView,MyFavOrgView,MyFavTeacherView,MyFavCourse,MyMessageView,SendMobileCodeView,ModifyMobileView,MyOrderView

urlpatterns = [
	path('login/',LoginView.as_view(),name='login'),
	path('logout/',LogoutView.as_view(),name='logout'),
	path('register/',RegisterView.as_view(),name='register'),
	path('captcha/',include('captcha.urls')),
	path('active/<str:active_code>/',ActiveUserView.as_view(),name='active_user'),
	path('forgetpassword/',ForgetPasswordView.as_view(),name='forgetpassword'),
	path('reset/<str:active_code>/',ResetView.as_view(),name='reset'),
	#忘记密码界面修改密码
	path('modifypassword/',ModifyPasswordView.as_view(),name='modifypassword'),
	path('user_info/',UserCenterInfoView.as_view(),name='user_info'),
	path('modify_useravater/',UserAvaterUploadView.as_view(),name='modify_useravater'),
	#个人中心页面修改密码
	path('update_password/',UpdatePasswordView.as_view(),name='update_password'),
	#个人中心页面发送验证码
	path('send_verifycode/',SendVerifyCodeView.as_view(),name='send_verifycode'),
	path('modify_email/',ModifyEmailView.as_view(),name='modify_email'),
	path('mycourses/',MyCourseView.as_view(),name='mycourses'),
	path('myfav/org/',MyFavOrgView.as_view(),name='myfav_org'),
	path('myfav/teacher/',MyFavTeacherView.as_view(),name='myfav_teacher'),
	path('myfav/course/',MyFavCourse.as_view(),name='myfav_course'),
	path('messages/',MyMessageView.as_view(),name='messages'),
	path('myorders/',MyOrderView.as_view(),name='myorders'),
	path('send_mobilecode/',SendMobileCodeView.as_view(),name='send_mobilecode'),
	path('modify_mobile/',ModifyMobileView.as_view(),name='modify_mobile'),
	
]