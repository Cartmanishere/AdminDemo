
from django.conf.urls import url, include
from django.contrib import admin
from demo import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_maid/$', views.add_maid, name='add_maid'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^view/(?P<id>\d+)/$', views.view_maid, name='view_maid'),
    url(r'^delete/maid/(?P<id>\d+)/$', views.delete_maid, name='delete_maid'),
    url(r'^delete/agent/(?P<id>\d+)/$', views.delete_agent, name='delete_agent'),
    url(r'^signup/agent/$', views.signup_agent, name='signup_agent'),
    url(r'^signup/admin/$', views.signup_admin, name='signup_admin'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^agents/$', views.agent_index, name='agent_index'),
    url(r'^profile/agent/$', views.agent_profile, name='agent_profile'),
    url(r'^profile/admin/$', views.admin_profile, name='admin_profile'),
]


