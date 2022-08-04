from django.shortcuts import render
from django.http import HttpResponse

#前台首页
def index(request):
    return HttpResponse('欢迎进入大堂点餐前台首页！')