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

from Show import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^test/',views.test),

    url(r'^404',views.pagenotfound),
    url(r'^index',views.index),
    url(r'^control', views.control),
    url(r'^log',views.logging),
    url(r'^setting', views.setting),
    url(r'^help', views.help),
    url(r'^odlsetting',views.odlsetting),

    # ODL setting 部分
    url(r'^ajax_odlsetting_stop',views.ajax_odlsetting_stop),
    url(r'^ajax_odlsetting_start',views.ajax_odlsetting_start),
    url(r'^ajax_odlsetting_change',views.ajax_odlsetting_change),
    url(r'^ajax_odlsetting_getlog',views.ajax_odlsetting_getlog),
]
