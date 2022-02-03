from django.urls import path
from django.conf.urls import url

from . import views
from afl_events import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.contrib import admin
from afl_events.views import addEvent,PayAmount

app_name = 'afl_events'


urlpatterns = [
    # url(r'^registration',views.index),


    url(r'^login_user',views.login_user,name='login_user'),

    url(r'^test',views.test,name='test'),
    # url(r'^login_user',views.login_user,name='login_user'),

    # url(r'^admin_login',views.admin_login,name='admin_login'),
    url(r'^login_admin',views.login_admin,name='login_admin'),

    # url(r'^admin_home',views.admin_home,name='admin_home'),
    url(r'^user_home',views.user_home,name='user_home'),

    url(r'^user_event',views.user_event,name='user_event'),
    # url(r'^ground_booking',views.ground_booking,name='ground_booking'),
    # url(r'^db_ground_booking',views.db_ground_booking,name='db_ground_booking'),

    # url(r'^admin_booking',views.admin_booking,name='admin_booking'),
    # url(r'^admin_event',views.admin_event,name='admin_event'),

    # url(r'^update_event/(?P<id>\d+)/$',views.update_event,name='update_event'),
    # url(r'^db_update_event/(?P<id>\d+)/$',views.db_update_event,name='db_update_event'),
    # url(r'^db_delete_event/(?P<id>\d+)/$',views.db_delete_event,name='db_delete_event'),

    # url(r'^add_event',views.add_event,name='add_event'),
    # url(r'^db_add_event',views.db_add_event,name='db_add_event'),

    url(r'^user_logout',views.user_logout,name='user_logout'),
    # url(r'^admin_logout',views.admin_logout,name='admin_logout'),
    url(r'^nsbtest/', views.testcodensb,name='testcode'),


    # -------------------------------------------------
    path('admin/', admin.site.urls),
    url(r'^user-registration',views.register_view,name='registration'),
    # Login and Logout
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'
        ), 
        name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(
            next_page='afl/homepage'
        ), 
        name='logout'
    ),
    # path('homepage', TemplateView.as_view(template_name='home.html'), name='homepage'),
    url('homepage/', views.user_home, name='homepage'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'), # new
    path('post/ajax/add_event', addEvent, name = "add_event"),
    url(r'^add-payment/(?P<e_id>\d+)/$', PayAmount.as_view(), name='pay_amount'),
]