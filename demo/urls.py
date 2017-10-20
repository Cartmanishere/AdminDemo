
from django.conf.urls import url, include
from django.contrib import admin
from demo import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_maid/$', views.add_maid, name='add_maid'),
    url(r'^login/$', views.login_user, name='login'),
]


