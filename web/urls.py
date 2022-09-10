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
# myobject/web/urls.py

from django.urls import path

from web.views import index

urlpatterns = [
   path('', index.index, name="index"),

   #短信登录账户
   path('login/sms/', index.login_sms, name="web_login_sms"),
   #注册账户
   path('register/', index.register, name="web_register"),
   #发送短信
   path('send/sms/', index.send_sms, name="web_send_sms"),#短信

]