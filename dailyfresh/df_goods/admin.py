#coding=utf-8
from __future__ import unicode_literals
# Register your models here.
from django.contrib import admin
# Register your models here
from models import *
# Register your models here.


class TypeInfoAdmin(admin.ModelAdmin):
    list_display=['id','ttitle']


class GoodsInfoAdmin(admin.ModelAdmin):
    list_per_page=15
    #外建关联的那个自段不需要写入进去,不然要报错
    list_display = ['id', 'gtitle', 'gprice', 'gclick','gunit', 'gkucun', 'gcontent','gtpye']

admin.site.register(TypeInfo,TypeInfoAdmin)
admin.site.register(GoodsInfo,GoodsInfoAdmin)

