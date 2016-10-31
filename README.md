# A_Simple_Back_Word_Website
A simple site to back word built with the Python and Django frameworks.

在线访问网址：http://word.chaiziyi.com.cn/

> 假设你现在想做一个简单的背单词应用，具体提供下面的4项功能：

> 1. 用户可以根据自己的英语水平，例如 四级，六级，雅思，和托福 来设置自己背单词的范围；
> 2. 每个用户可以设置每天背多少单词
> 3. 用户背单词过程中能够添加笔记， 也可以查看其他用户共享的笔记
> 4. 用户背单词过程中，可以看到单词，单词的解释和例句。

> 我们要求作业用 Python, 最好是 基于 Django 框架来完成， Web 页面可以基于 bootstrap 来简化你的开发流程。

----------

以上是面试扇贝网后端时面试官给我布置的小任务，花了三天基本上算是做完了，主要做了注册、登录、主页、个人信息页和背单词页等5个页面，数据库的Word表里面的单词和释义数据是找的网上的，但只导入了1000个用来测试，例句就是随便写的了。用户在个人信息页可以设置背单词的范围以及每天背多少单词，网站的主要功能在背单词页，点击下一个按钮会根据用户设定的范围随机呈现一个单词，用户也可以在单词页对该单词添加笔记，笔记所有用户共享。最后对表单提交的数据做了一下简单的过滤，数据库用的是Python自带的sqlite3。对于要清空的每天已背单词数的那个值，查了一下，好像用Django-crontab这个第三方库可以实现，但是在windows好像不能运行，之前也没用过，也不知道部署到服务器上能不能成功。

**10.30更新**

花了点时间把小网站部署到Ubuntu服务器上了，用的是nginx+uwsgi的方式。不过还是有两个小问题，一个是Django的DEBUG模式关不掉，关掉的话nginx就会显示Request Bad(400)错误，还有一个昨天说的Django-crontab这个库的问题老是提示找不到，暂时也没能找到解决办法，大概就是这样。

**10.31再更新**

昨天说的DEBUG不能设置为False的问题解决了，原来是忘了在setting.py中加ALLOWED_HOSTS了，加上去就OK了，还有找不到Django-crontab是因为我在INSTALLED_APPS里面写成了'django-crontab'，而事实上应该写成'django_crontab'，连接符和下划线怎么差别就这么大呢？定时任务已经加载进去了，具体效果还得过了12点才能看到。另外，还改了一个登录的小bug，之前没有判断用户名是否在数据库就直接get了，所以如果本来没有这个用户名就会抛异常（囧……

## 主页
![](http://i.imgur.com/heIfOrP.png)

## 注册页面
![](http://i.imgur.com/3eRbZcY.png)

## 登录页面
![](http://i.imgur.com/3MC1zLZ.png)

## 个人信息页
![](http://i.imgur.com/ZYi5w5c.png)

## 背单词页
![](http://i.imgur.com/UGakkgT.png)
