from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, Word, Note, Example
#from django.contrib.auth.decorators import login_required
import hashlib
from django.contrib.auth import authenticate, login, logout
from random import choice
#from django.db.models import Q
from itertools import chain

# 主页
def index(request):
    return render(request, 'index.html')

# 注册页面
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        if User.objects.filter(username=username):
            isregistered = True                 # 已被注册
        else:
            isregistered = False                # 未被注册
            password = add_password(request.POST['password'])
            user = User.objects.create(
                username=username, password=password)
            request.session['username'] = user.username
            return redirect('/')
    return render(request, 'register.html',locals())

# 登录页面
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = add_password(request.POST['password'])
        # user = authenticate(username=username, password=password)
        if User.objects.filter(username=username):
            user_obj = User.objects.get(username=username)
            if user_obj.password==password:
                iscorrect = True                    # 登录成功
                request.session['username'] = username
                return redirect('/')
            else:
                iscorrect = False                   # 登录失败
                return render(request, 'login.html',locals())
        else:
            iscorrect = False                   # 登录失败
            return render(request, 'login.html',locals())
    else:
        if request.session.get('username',False):
            return redirect('/')
        else:
            iscorrect = True
            return render(request, 'login.html',locals())
# 登出
def logout_view(request):
    del request.session['username']     # 删除session里面的用户名
    return redirect('/')

# 密码用md5加密
def add_password(password):
    password_md5 = hashlib.md5(password.encode('utf-8')).hexdigest()
    return password_md5

# 个人信息页面
def info_view(request):
    if request.method == 'GET':
        if request.session.get('username',False):
            username = request.session['username']
            user_obj = User.objects.get(username=username)
            isselectCET4 = user_obj.selectCET4
            isselectCET6 = user_obj.selectCET6
            isselectIELTS = user_obj.selectIELTS
            isselectTOEFL = user_obj.selectTOEFL
            daynum = user_obj.daynum
            dayrecitednum = user_obj.dayrecitednum
            return render(request, 'info.html',locals())
        else:
            return redirect('/login')
    else:
        wordrangelist = request.POST.getlist('wordrange')
        daynum = request.POST.get('daynum',False)
        username = request.session['username']
        user_obj = User.objects.get(username=username)
        if daynum:
            if daynum.isdigit() and int(daynum) in range(1,201):
                user_obj.daynum = daynum
                changeWordrange(user_obj,wordrangelist)
                return redirect('/')
            else:
                daynumerror = True
                isselectCET4 = user_obj.selectCET4
                isselectCET6 = user_obj.selectCET6
                isselectIELTS = user_obj.selectIELTS
                isselectTOEFL = user_obj.selectTOEFL
                daynum = user_obj.daynum
                dayrecitednum = user_obj.dayrecitednum
                return render(request, 'info.html',locals())
        else:
            changeWordrange(user_obj,wordrangelist)
            return redirect('/')
          
# 背单词页面
def backword_view(request):
    if request.method == 'GET':
        if request.session.get('username',False):
            username = request.session['username']
            user_obj = User.objects.get(username=username)
            isselectCET4 = user_obj.selectCET4
            isselectCET6 = user_obj.selectCET6
            isselectIELTS = user_obj.selectIELTS
            isselectTOEFL = user_obj.selectTOEFL
            daynum = user_obj.daynum
            dayrecitednum = user_obj.dayrecitednum
            if not (isselectCET4 or isselectCET6 or isselectIELTS or isselectTOEFL):
                noselect = True
                return render(request, 'info.html',locals())
            else:
                remaining = daynum - dayrecitednum
                if remaining < 0:
                    isdone = True
                    muchmore = -remaining
                if request.session.get('wordid',False):
                    wordid = request.session['wordid']
                else:
                    w1 = w2 = w3 = w4 = ''
                    if isselectCET4:
                        w1 = Word.objects.filter(isCET4=isselectCET4)
                    if isselectCET6:
                        w2 = Word.objects.filter(isCET6=isselectCET6)
                    if isselectIELTS:
                        w3 = Word.objects.filter(isIELTS=isselectIELTS)
                    if isselectTOEFL:
                        w4 = Word.objects.filter(isTOEFL=isselectTOEFL)
                    words = list(chain(w1,w2,w3,w4))
                    wordid = choice(words).id
                    request.session['wordid'] = wordid
                selectword = Word.objects.get(id=wordid)
                word = selectword.word
                interpretation = selectword.interpretation
                isCET4 = selectword.isCET4
                isCET6 = selectword.isCET6
                isIELTS = selectword.isIELTS
                isTOEFL = selectword.isTOEFL
                example = Example.objects.filter(wordid=wordid)
                if example:
                    examplelist = list()
                    for item in example:
                        templist = list()
                        templist.append(item.exampleen)
                        templist.append(item.examplezh)
                        examplelist.append(templist)
                note = Note.objects.filter(wordid=wordid)
                if note:
                    notelist = list()
                    for item in note:
                        templist = list()
                        templist.append(item.username)
                        templist.append(item.note)
                        notelist.append(templist)
                return render(request, 'backword.html',locals())
        else:
            return redirect('/login')
    else:
        if request.session.get('wordid',False):
            del request.session['wordid']
        if request.session.get('username',False):
            username = request.session['username']
            user_obj = User.objects.get(username=username)
            user_obj.dayrecitednum = int(request.POST.get('dayrecitednum',False))+1 # 已背诵单词数加1
            user_obj.save()
        return redirect('/backword')

# 添加笔记的跳转页面
def addnote(request):
    if request.method == 'POST' and request.session.get('username',False):
        username = request.session['username']
        note = request.POST.get('note',False)
        wordid = request.POST.get('wordid',False)
        request.session['wordid'] = wordid
        Note.objects.create(username=username,note=note,wordid_id=wordid)
        return redirect('/backword')

def changeWordrange(user_obj,wordrangelist):
    if 'CET4' in wordrangelist:
        user_obj.selectCET4 = True
    else:
        user_obj.selectCET4 = False
    if 'CET6' in wordrangelist:
        user_obj.selectCET6 = True
    else:
        user_obj.selectCET6 = False
    if 'IELTS' in wordrangelist:
        user_obj.selectIELTS = True
    else:
        user_obj.selectIELTS = False
    if 'TOEFL' in wordrangelist:
        user_obj.selectTOEFL = True
    else:
        user_obj.selectTOEFL = False
    user_obj.save()
    return True