from django.http import HttpResponse
from django.shortcuts import render,HttpResponse
from web.forms.account import RegisterModelForm,SendSmsForm,LoginSmsForm
from django.http import JsonResponse
import random
from utils.tencent.sms import send_sms_single
from django.conf import settings
from web import models

"""
用户账户相关功能：注册，短信，登录，注销

"""
def index(request):
    """前台首页"""
    return render(request, 'web/index/index.html')


def register(request):
    """注册账户"""
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'web/index/register.html', {'form': form})
    print(request.POST)
    form =RegisterModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True , 'data': '/login/sms/'})
    return JsonResponse({'status': False , 'error': form.errors})


def login_sms(request):
    """短信登录"""
    if request.method =='GET':
        form = LoginSmsForm()
        print(form)
        return render(request, 'web/index/login_sms.html', {'form':form})
    form = LoginSmsForm(request.POST)
    if form.is_valid():

        #用户输入正确，登录成功
        mobile_phone = form.cleaned_data['mobile_phone']
        print(mobile_phone)
        #用户信息放入session
        user_object=models.UserInfo.objects.filter(mobile_phone=mobile_phone).first()
        print(user_object)
        request.session['user_id'] = user_object.id
        request.session['user_name'] =user_object.username

        return JsonResponse({'status': True,'data': "/index/"})
    return JsonResponse({'status': False, 'error': form.errors})

def login(request):
    """用户名和密码登录"""



def send_sms(request):
    """发送短信"""
    form = SendSmsForm(request,data=request.GET)
    print(form)
    #只是校验手机号：不能为空、格式是否正确
    if form.is_valid():
        #发短信
        #写redis
        return JsonResponse({'status':True})
    return JsonResponse({'status':False,'error':form.errors})

    # template_id=settings.TENCENT_SMS_TEMPLATE.get(tpl)
    # if not template_id:
    #     return HttpResponse('模板不存在')
    # code = random.randrange(1000,9999)
    # res=send_sms_single('15131255089',template_id,[code,])
    # if res['result'] == 0:
    #     return HttpResponse('成功')
    # else:
    #     return HttpResponse(res['errmsg'])







