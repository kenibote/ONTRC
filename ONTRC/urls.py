"""ONTRC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from Show import views,\
    viewODLsetting,viewOEOsetting,viewWSSsetting,\
    viewControl

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^test/',views.test),

    # 主页面
    url(r'^404',views.pagenotfound),
    url(r'^index',views.index),
    url(r'^log',views.logging),
    url(r'^setting', views.setting),
    url(r'^help', views.help),

    # Control 部分
    url(r'^control', viewControl.control),
    url(r'^ajax_control_loadoeoinfo',viewControl.ajax_control_loadoeoinfo),
    url(r'^ajax_control_updataoeoinfo',viewControl.ajax_control_updataoeoinfo),


    # ODL setting 部分
    url(r'^odlsetting',viewODLsetting.odlsetting),
    url(r'^ajax_odlsetting_stop',viewODLsetting.ajax_odlsetting_stop),
    url(r'^ajax_odlsetting_start',viewODLsetting.ajax_odlsetting_start),
    url(r'^ajax_odlsetting_change',viewODLsetting.ajax_odlsetting_change),
    url(r'^ajax_odlsetting_getlog',viewODLsetting.ajax_odlsetting_getlog),

    # OEO setting 部分
    url(r'^oeosetting',viewOEOsetting.oeosetting),
    url(r'^ajax_oeosetting_stop',viewOEOsetting.ajax_oeosetting_stop),
    url(r'^ajax_oeosetting_start',viewOEOsetting.ajax_oeosetting_start),
    url(r'^ajax_oeosetting_change',viewOEOsetting.ajax_oeosetting_change),
    url(r'^ajax_oeosetting_getlog',viewOEOsetting.ajax_oeosetting_getlog),

    # WSS setting 部分
    url(r'^wsssetting',viewWSSsetting.wsssetting),

    # 对于空连接重定向至主页
    url(r'',views.NoneMainPage),
]
