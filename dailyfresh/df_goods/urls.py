#coding=utf-8
from django.conf.urls import url
import views

urlpatterns=[
    url(r'^index/$',views.index),
    url(r'^$',views.index),
    url(r'^list(\d+)_(\d+)_(\d+)/$',views.goodlist),
    url(r'^(\d+)/$', views.detail),
   # url(r'^base_foot/$',views.base_foot),
]