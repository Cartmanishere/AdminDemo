
from django.conf.urls import url, include
from django.contrib import admin
from demo import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_maid/$', views.add_maid, name='add_maid'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^view/(?P<id>\d+)/$', views.view_maid, name='view_maid'),
    url(r'^delete/(?P<id>\d+)/$', views.delete_maid, name='delete_maid'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', views.logout_user, name='logout')

]


