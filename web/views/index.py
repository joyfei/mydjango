from django.shortcuts import render,HttpResponse,redirect
from web.forms.account import RegisterModelForm,SendSmsForm,LoginSmsForm,loginForm
from django.http import JsonResponse
from web import models
import random
from utils.tencent.sms import send_sms_single
from django.conf import settings

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
    print('注册账户',request.POST)
    form =RegisterModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True , 'data': '/login/'})
    return JsonResponse({'status': False , 'error': form.errors})


def login_sms(request):
    """短信登录"""
    if request.method == 'GET':
        form = LoginSmsForm()
        print('短信登录',request.GET)
        return render(request, 'web/index/login_sms.html', {'form':form})
    form = LoginSmsForm(request.POST)
    if form.is_valid():

        #用户输入正确，登录成功
        mobile_phone = form.cleaned_data['mobile_phone']
        #用户信息放入session
        user_object=models.UserInfo.objects.filter(mobile_phone=mobile_phone).first()
        request.session['user_id'] = user_object.id
        request.session['user_name'] =user_object.username

        return JsonResponse({'status': True,'data': "/index/"})
    return JsonResponse({'status': False, 'error': form.errors})

def login(request):
    """用户名和密码登录"""
    if request.method == 'GET':
        form = loginForm(request)
        return render(request, 'web/index/login.html', {'form': form})
    form = loginForm(request,data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        from django.db.models import Q
        #  (手机=username and pwd=pwd) or (邮箱=username and pwd=pwd)
        user_object = models.UserInfo.objects.filter(Q(email=username) | Q(mobile_phone=username)).filter(password=password).first()

        if user_object:
            #用户名和密码正确
            return redirect('/index/')
        form.add_error('username','用户名或密码错误')
    return render(request, 'web/index/login.html', {'form': form})




def image_code(request):
    """生成图片验证码"""
    from io import BytesIO
    from utils.image_code import check_code

    image_object, code = check_code()
    print('验证码：',code)
    request.session['image_code']=code
    request.session.set_expiry(60) #主动修改session过期时间为60s

    stream =BytesIO()
    image_object.save(stream,'png')
    return HttpResponse(stream.getvalue())

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








