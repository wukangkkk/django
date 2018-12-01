#coding=utf-8

from django.http import HttpResponseRedirect
def islogin(func):
    """
    登录每一个页面都需要进行用户的验证,不然用户的信息很容易被泄露
    于是我们要用到装饰器的知识,不需要改变viwe内的函数,直接加上@islogin
    """
    def func_in(request,*args,**kwargs):
        if request.session.get('user_id'):
            return func(request,*args,**kwargs)
        else:
            red=HttpResponseRedirect('/user/login/')
            #保存我们想取页面的路径,一旦登入成功,就会跳转到这个页面来
            red.set_cookie('url',request.get_full_path())
            return red
    return func_in

'''
url=https://127.0.0.1:8000/200/?type=10
request.path:表示路径为/200
request.get_full_path() 表示完整路径 /200/?type=10
'''