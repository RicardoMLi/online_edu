"""Mxonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin

from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from .views import IndexView

urlpatterns = [
    path('',IndexView.as_view(),name='index'),
    path('xadmin/', xadmin.site.urls),
    path('user/',include('user.urls')),
    path('organization/',include('organization.urls')),
    path('user_operation/',include('user_operation.urls')),
    path('course/',include('course.urls')),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

#全局404错误处理函数
handler404 = 'Mxonline.views.page_not_found'

#全局500错误处理函数
handler500 = 'Mxonline.views.page_error'