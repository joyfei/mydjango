from django.shortcuts import render,HttpResponse


#文件上传
def index(request):
    if request.method == "GET":
        return render(request,'myadmin/upload/index.html')
    print(request.POST)#请求体中的数据
    print(request.FILES)#请求发过来的文件
    file_object = request.FILES.get("avatar")
    print(file_object.name)
    f = open('static/uploads/'+file_object.name,mode='wb')
    for chunk in file_object.chunks():
        f.write(chunk)
    f.close()
    return render(request,'myadmin/upload/index.html')