#coding=utf-8
from django.shortcuts import render,redirect,HttpResponseRedirect
from hashlib import sha1  #加密引用hashlib
from models import *
from df_goods.models import GoodsInfo
from django.http import JsonResponse
from .islogin import islogin
# Create your views here.
def register(request):
    #注册页面
    return render(request,'df_user/register.html')

def register_handle(request):
    #接受用户输入
    post=request.POST
    uname=post.get('user_name')
    upwd=post.get('pwd')
    upwd2=post.get('cpwd')
    uemail=post.get('email')
    #判断密码2次是否一致
    if upwd !=upwd2:
        return redirect('/user/register/')
    #加密操作
    s1=sha1()
    s1.update(upwd)
    upwd3=s1.hexdigest()
    #创建对象.存储在数据库中
    user=UserInfo()
    user.uname=uname
    user.upwd=upwd3
    user.uemail=uemail
    user.save()
    #注册成功,转到登录页面
    return redirect('/user/login/')

# 判断用户是否已经存在
def register_exist(requset):
    #获取js传过来的名字数据
    uname = requset.GET.get('uname')
    #在数据库查找,并返回一个数值,不是0就是1
    print(uname)
    count = UserInfo.objects.filter(uname=uname).count()
    print(count)
    return JsonResponse({'count': count})
#登入的界面
def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 0, 'uname': uname}
    return render(request, 'df_user/login.html', context)

def login_handle(request):
    # 接收请求信息
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    #接收提交过来的返回值,默认值为0
    jizhu =post.get('jizhu', 0)
    # 根据用户名查询对象,用objects.get查不到会抛出异常,filter查不到返回[]
    users = UserInfo.objects.filter(uname=uname)
    if len(users) == 1:
        s1 = sha1()
        s1.update(upwd)
        # 登录带cookie值必须red = HttpResponseRedirect
        #    red.set_cookie  renturn red
        if s1.hexdigest() == users[0].upwd:
            #取出要登录的页面,取出存入的cookie值
            url=request.COOKIES.get('url','/index/')
            red = HttpResponseRedirect(url)
            # 记住用户名
            if jizhu != 0:
                #写入cookie
                red.set_cookie('uname', uname)
            else:
                #把uname的值清空,-1立马清空,60表示60秒后过期
                red.set_cookie('uname', '', max_age=-1)
            #在我们登录的时候,我们就写入session信息,记录下id和uname
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname

            return red
        else:
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname}
        return render(request, 'df_user/login.html', context)
#登录后的页面
@islogin
def info(request):
    user_email=UserInfo.objects.get(id=request.session['user_id']).uemail
    #最近浏览
    # 最近浏览
    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_id_list = goods_ids.split(',')
    goods_list = []
    if len(goods_ids):
        for goods_id in goods_id_list:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))

    context = {'title': '用户中心',
               'user_email': user_email,
               'user_name': request.session['user_name'],
               'page_name': 1, 'info': 1,
               'goods_list': goods_list}
    return render(request,'df_user/user_center_info.html',context)
@islogin
def order(request):
    context={'title':'用户中心',
             'user_name': request.session['user_name']
             }
    return render(request,'df_user/user_center_order.html',context)

@islogin
def site(request):
    user=UserInfo.objects.get(id=request.session['user_id'])
    if request.method=='POST':
        post=request.POST
        user.ushou=post.get('ushou')
        user.uaddress=post.get('uaddress')
        user.uyoubian=post.get('uyoubian')
        user.uphone=post.get('uphone')
        user.save()
    context={'title':'用户中心',
             'user':user,
             'user_name': request.session['user_name']
             }
    return render(request,'df_user/user_center_site.html',context)
def logout(request):
    #清除session,从新登录
    request.session.flush()
    return redirect('/')

