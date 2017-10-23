
from django.conf.urls import url, include
from django.contrib import admin
from demo import views


urlpatterns = [
    url(r'^$', views.maid_index, name='maid_index'),
    url(r'^agent/add_maid/$', views.add_maid, name='agent_add_maid'),
    url(r'^admin/add_maid/$', views.add_maid, name='admin_add_maid'),
    url(r'^agent/$', views.index_gent, name='agent_index'),
    url(r'^admin/$', views.index_dmin, name='agent_index'),
    url(r'^admin/login/$', views.login_user, name='admin_login'),
    url(r'^agent/login/$', views.login_user, name='admin_login'),
    url(r'^login/$', views.login_user, name='customer'),
    url(r'^view/(?P<id>\d+)/$', views.view_maid, name='view_maid'),
    url(r'^delete/maid/(?P<id>\d+)/$', views.delete_maid, name='delete_maid'),
    url(r'^delete/agent/(?P<id>\d+)/$', views.delete_agent, name='delete_agent'),
    url(r'^delete/customer/(?P<id>\d+)/$', views.delete_customer, name='delete_customer'),
    url(r'^delete/request/(?P<id>\d+)/$', views.delete_request, name='delete_request'),

    url(r'^admin/add_agent/$', views.signup_agent, name='signup_agent'),
    #url(r'^signup/admin/$', views.signup_admin, name='signup_admin'),
    url(r'^signup/customer/$', views.signup_customer, name='signup_customer'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^admin/agents/$', views.agent_index, name='agent_index'),
    url(r'^admin/customers/$', views.customer_index, name='customer_index'),
    url(r'^requests/$', views.request_index, name='request_index'),
    url(r'^requests/new/$', views.request_add, name='request_add'),
    url(r'^requests/status/change/$', views.status_change, name='status_change'),
    url(r'^agent/profile/$', views.agent_profile, name='agent_profile'),
    url(r'^admin/profile/$', views.admin_profile, name='admin_profile'),
    url(r'^profile/customer/$', views.customer_profile, name='customer_profile'),
    url(r'^profile/customer/(?P<id>\d+)/$', views.customer_profile, name='customer_profile'),
    url(r'^profile/agent/(?P<id>\d+)/$', views.agent_profile, name='agent_profile'),
    url(r'^admin/statistics/$', views.statistics, name='statistics'),

    #url(r'^maid_index/$',views.index,name='index'),

]


