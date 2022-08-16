from django.http import HttpResponse
from django.shortcuts import render,HttpResponse
from web.forms.account import RegisterModelForm,SendSmsForm
from django.http import JsonResponse
import random
from utils.tencent.sms import send_sms_single
from django.conf import settings

"""
用户账户相关功能：注册，短信，登录，注销

"""
def index(request):
    """前台首页"""
    return render(request, 'web/index/index.html')


def send_sms(request):
    """发送短信"""
    form = SendSmsForm(request,data=request.GET)
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



def register(request):
    """注册账户"""
    form = RegisterModelForm()
    return render(request, 'web/index/register.html', {'form':form})