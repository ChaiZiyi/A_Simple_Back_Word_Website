from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, Word, Note, Example
from django.contrib.auth.decorators import login_required
import hashlib

def index(request):
    return render(request, 'index.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        if User.objects.filter(username=username):
            return HttpResponse('用户已存在!')
        else:
            password = add_password(request.POST['password'])
            user = User.objects.create(
                username=username, password=password,)
            request.session['username'] = user.username
            return redirect('/backwordweb/')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = add_password(request.POST['password'])
        user_objs = User.objects.filter(username=username)
        if len(user_objs) == 1:
            user = user_objs[0]
            request.session['username'] = user.username
            return redirect('/backwordweb/')
        else:
            return HttpResponse('用户不存在或者密码账号输入不正确')
    else:
        return render(request, 'login.html')
    return render(request, 'index.html')


def logout_view(request):
    del request.session
    return render(request, 'index.html')


def add_password(password):
    password_md5 = hashlib.md5(password.encode('utf-8')).hexdigest()
    return password_md5
