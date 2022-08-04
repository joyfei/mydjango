from django.shortcuts import render
from django.http import HttpResponse

#用户管理
def index(request):
    '''管理后台首页'''
    return render(request, "myadmin/user/index.html")



