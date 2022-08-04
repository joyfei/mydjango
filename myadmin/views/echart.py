from django.shortcuts import render
from django.http import HttpResponse

#后台首页
def index(request):
    '''管理后台首页'''
    return render(request, "myadmin/echart/index.html")