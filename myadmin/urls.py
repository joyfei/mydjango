"""MyDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
# myobject/myadmin/urls.py

from django.urls import path

from myadmin.views import index,user,site,role,echart,upload

urlpatterns = [
    # 后台首页
    path('', index.index, name="myadmin_index"),
    #用户管理
    path('user/', user.index, name="myadmin_user_index"),#浏览

    #角色管理
    path('role/', role.index, name="myadmin_role_index"),#浏览

    #图表管理
    path('echart/', echart.index, name="myadmin_echart_index"),  # 浏览

    #设置管理
    path('site/', site.index, name="myadmin_site_index"),#浏览

    #文件上传
    path('upload/list', upload.index, name="myadmin_upload_index"),#浏览

]