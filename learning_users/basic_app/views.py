from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoModel, UserProfileInfoForm
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
# 要使用装饰器必须要先import
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return  render(request,'basic_app/index.html')

def special(request):
    return HttpResponse("You are logged in! Nice!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
    # 'index'是在urls.py中定义的name,而urls中的index指向了views.index这个函数，结果就是返回index.html界面

def register(request):

    registered= False

    if request.method == "POST": #如果用户传入了信息
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        # request.POST: 一个类似字典的对象，包含所有给定的 HTTP POST 参数，前提是请求包含表单数据。

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            # save() 方法接受一个可选参数 commit ，它的值是 True 或者 False 。
            # 如果调用 save() 的时候使用 commit=False ，那么它会返回一个尚未保存到数据库的对象。
            # 在这种情况下，需要您自己在生成的模型实例上调用 save() 。
            # 如果要在保存对象之前对对象执行自定义操作，或者要使用其中一个专用的模型保存选项 ，这很有用。
            # commit 的值默认为 True 。

            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            """
            HttpRequest.FILES: 一个类似字典的对象，包含所有上传的文件。
            FILES 中的每个键是 <input type="file" name=""> 中的 name。
            FILES 中的每个值是一个 UploadedFile。
            FILES 只有在请求方法是 POST,
            并且发布请求的 <form> 有 enctype="multipart/form-data" 的情况下，
            才会包含数据。否则，FILES 将是一个类似字典的空白对象。
            """

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html',
                            {'user_form': user_form,
                            'profile_form':profile_form,
                            'registered':registered})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request, user)
                #如果有一个已验证的用户想附加到当前会话(session)中，将通过 login()完成。
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("Account not active!")

        else:
            print("Login faliled! ")
            print("Username:{} and password: {}".format(username, password))
            return HttpResponse("Invalid login details supplied! ")

    else:
        return render(request,'basic_app/login.html',{})
