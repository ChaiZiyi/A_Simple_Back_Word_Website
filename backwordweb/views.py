from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, Word, Note, Example
#from django.contrib.auth.decorators import login_required
import hashlib
from django.contrib.auth import authenticate, login, logout
from random import choice

def index(request):
    return render(request, 'index.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        if User.objects.filter(username=username):
            isregistered = True
        else:
            isregistered = False
            password = add_password(request.POST['password'])
            user = User.objects.create(
                username=username, password=password)
            request.session['username'] = user.username
            return redirect('/')

    return render(request, 'register.html',locals())


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = add_password(request.POST['password'])
        user = authenticate(username=username, password=password)
        user_objs = User.objects.filter(username=username)
        if len(user_objs) == 1:
            iscorrect = True
            user = user_objs[0]
            request.session['username'] = user.username
            return redirect('/')
        else:
            iscorrect = False
            return render(request, 'login.html',locals())
    else:
        if request.session.get('username',False):
            return redirect('/')
        else:
            iscorrect = True
            return render(request, 'login.html',locals())

def logout_view(request):
    del request.session['username']
    return redirect('/')


def add_password(password):
    password_md5 = hashlib.md5(password.encode('utf-8')).hexdigest()
    return password_md5

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
            user_obj.daynum = daynum
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
        return redirect('/info')

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
                words = Word.objects.filter(isCET4=isselectCET4,isCET6=isselectCET6,
                    isIELTS=isselectIELTS,isTOEFL=isselectTOEFL)
                wordid = choice(words).id
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
                    for item in example:
                        templist = list()
                        templist.append(item.username)
                        templist.append(item.note)
                        notelist.append(templist)
                return render(request, 'backword.html',locals())
        else:
            return redirect('/login')