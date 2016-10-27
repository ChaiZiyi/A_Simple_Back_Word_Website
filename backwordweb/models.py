from django.db import models
from django.contrib.auth.models import AbstractUser

# 用户表
class User(AbstractUser):

    id = models.AutoField(primary_key=True)             #用户id
    selectCET4 = models.BooleanField(default=False)     #用户是否选择了四级
    selectCET6 = models.BooleanField(default=False)     #用户是否选择了六级
    selectIELTS = models.BooleanField(default=False)    #用户是否选择了雅思
    selectTOEFL = models.BooleanField(default=False)    #用户是否选择了托福
    daynum = models.IntegerField(default=50)            #用户设置的每天要背的单词个数
    dayrecitednum = models.IntegerField(default=0)      #用户当天已经背的单词个数

    def __str__(self):
        return self.id

# 单词表
class Word(models.Model):

    id = models.AutoField(primary_key=True)             #单词id
    word = models.CharField(max_length=50)              #单词名
    interpretation = models.CharField(max_length=100)   #单词释义
    isCET4 = models.BooleanField()                      #单词是否属于四级词汇
    isCET6 = models.BooleanField()                      #单词是否属于六级词汇
    isIELTS = models.BooleanField()                     #单词是否属于雅思词汇
    isTOEFL = models.BooleanField()                     #单词是否属于托福词汇

    def __str__(self):
        return self.id

# 笔记表
class Note(models.Model):

    id = models.AutoField(primary_key=True)             #笔记id
    wordid = models.ForeignKey('Word')                  #单词id(外键)
    username = models.CharField(max_length=20)          #该笔记的用户名
    note = models.TextField(max_length=200)             #该笔记的内容

    def __str__(self):
        return self.id

# 例句表
class Example(models.Model):

    id = models.AutoField(primary_key=True)             #例句id
    wordid = models.ForeignKey('Word')                  #单词id(外键)
    exampleen = models.TextField(max_length=200)        #该例句
    examplezh = models.TextField(max_length=200)        #该例句的中文翻译

    def __str__(self):
        return self.id
