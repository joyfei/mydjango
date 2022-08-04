from django.shortcuts import render
from django.http import HttpResponse

#角色管理
def index(request):
    '''角色管理首页'''
    return render(request, "myadmin/role/index.html")