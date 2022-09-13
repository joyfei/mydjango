import random
from web import models
from django import forms
from django.conf import settings
from web.forms.bootstrap import BootStrapForm
from utils.tencent.sms import send_sms_single
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django_redis import get_redis_connection
from utils import encrypt



class RegisterModelForm(BootStrapForm,forms.ModelForm):
    mobile_phone=forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$','手机格式错误'),])
    password = forms.CharField(label='密码',
                               min_length=8,
                               max_length=64,
                               error_messages={
                                   'min_length': "密码长度不能小于8个字符",
                                   'max_length': "密码长度不能大于64个字符"
                                },
                               widget=forms.PasswordInput(attrs={'placeholder':'请输入密码'}))
    confirm_password =forms.CharField(label='重复密码',
                                      min_length=8,
                                      max_length=64,
                                      error_messages={
                                          'min_length': "重复密码长度不能小于8个字符",
                                          'max_length': "重复密码长度不能大于64个字符"
                                      },
                                      widget=forms.PasswordInput(attrs={'placeholder':'请输入重复密码'}))
    code = forms.CharField(label='验证码', widget=forms.TextInput(attrs={'placeholder':'请输入验证码'}))
    class Meta:
        model = models.UserInfo
        # fields = "__all__"
        fields =['username','email','password','confirm_password','mobile_phone','code']

    # def __init__(self,*args,**kwargs):
    #     super().__init__(*args, **kwargs)
    #     for name,field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'
    #         field.widget.attrs['placeholder'] = '请输入%s' %(field.label,)

    def clean_username(self):
        username = self.cleaned_data['username']
        exists=models.UserInfo.objects.filter(username=username).exists()
        if exists:
            raise ValidationError('用户名已存在')
        return username
    def clean_email(self):
        email = self.cleaned_data['email']
        exists=models.UserInfo.objects.filter(email=email).exists()
        if exists:
            raise ValidationError('邮箱已存在')
        return email
    def clean_password(self):
        password = self.cleaned_data['password']
        #加密返回
        return encrypt.md5(password)
    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = encrypt.md5(self.cleaned_data['confirm_password'])
        if password !=confirm_password:
            raise ValidationError('两次密码不一样')
        return confirm_password

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        exists =models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if exists:
            raise ValidationError('手机号已注册')
        return mobile_phone

    def clean_code(self):
        code = self.cleaned_data['code']
        mobile_phone = self.cleaned_data['mobile_phone']

        conn= get_redis_connection()
        redis_code = conn.get(mobile_phone)
        if not redis_code:
            raise ValidationError('验证码失效或未发送，请重新发送')
        redis_str_code=redis_code.decode('utf-8')

        if code.strip() != redis_str_code.strip():
            raise ValidationError('验证码错误，请重新输入')
        return code

class SendSmsForm(forms.Form):
    mobile_phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机格式错误'), ])

    def __init__(self, request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request =request

    def clean_mobile_phone(self):
        """手机号校验的钩子"""
        mobile_phone = self.cleaned_data['mobile_phone']

        #判断短信模板是否有问题
        tpl= self.request.GET.get('tpl')
        template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
        if not template_id:
            # self.add_error('mobile_phone','短信模板错误')
            raise ValidationError('短信模板错误')

        # 校验数据库中是否已有手机号
        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if tpl == 'login':
            if not exists:
                raise ValidationError('手机号不存在')
        else:
            if exists:
                raise ValidationError('手机号已存在')

        code =random.randrange(1000,9999)
        print('code:',code)
        #发送短信
        sms = send_sms_single(mobile_phone,template_id ,[code,])
        if sms['result'] != 0:
            raise ValidationError("短信发送失败,{}".format(sms['errmsg']))

        #验证码写入redis(django-redis)
        conn = get_redis_connection()
        conn.set(mobile_phone,code, ex=60)

        return mobile_phone

class LoginSmsForm(BootStrapForm,forms.Form):

    mobile_phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机格式错误'), ])
    code = forms.CharField(label='验证码', widget=forms.TextInput(attrs={'placeholder': '请输入验证码'}))

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        # user_object = models.UserInfo.objects.filter(mobile_phone=mobile_phone).first()
        if not exists:
            raise ValidationError('手机号不存在')
        return exists

    def clean_code(self):
        code = self.cleaned_data['code']
        mobile_phone = self.cleaned_data.get('mobile_phone')

        #手机号不存在，则验证码无需再校验
        if not mobile_phone:
            return code

        # 验证码写入redis(django-redis)
        conn = get_redis_connection()
        redis_code = conn.get(mobile_phone)
        if not redis_code:
            raise ValidationError('验证码失效或未发送，请重新发送')
        redis_str_code = redis_code.decode('utf-8')
        if code.strip() != redis_str_code.strip():
            raise ValidationError('验证码错误，请重新输入')
        return code


class loginForm(BootStrapForm,forms.Form):
    username=forms.CharField(label='邮箱或手机号')
    password=forms.CharField(label='密码',widget=forms.PasswordInput())
    code = forms.CharField(label='图片验证码')

    def __init__(self,request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_code(self):
        """钩子 图片验证码是否正确"""
        # 读取用户输入的验证码
        code = self.cleaned_data['code']
        #去session获取自己的验证码
        session_code = self.request.session.get('image_code')

        if not session_code:
            raise ValidationError('验证码已过期，请重新获取')

        if code.strip().upper() != session_code.strip().upper():
            raise ValidationError('验证码输入错误')
        return code

    def clean_password(self):
        password = self.cleaned_data['password']
        #加密返回
        return encrypt.md5(password)

