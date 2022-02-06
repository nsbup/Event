from django.urls import path
from django.conf.urls import url

from . import views
from afl_events import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.contrib import admin
from afl_events.views import addEvent,PayAmount
from django.conf.urls import include
# from afl_events.checkout import create_checkout_session
# from django.conf.urls import include, path

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
    # url(r'^checkout/(?P<e_id>\d+)/$', views.Payment_details.as_view(), name='checkout_page'),
    path('checkout/', views.Payment_details.as_view(), name='checkout_page_default'),
    path('checkout/<str:service>', views.Payment_details.as_view(), name='checkout_page'),

    # url(r'^checkout/(?P<e_id>\d+)/$',views.Payment_details.as_view(),name='checkout_page'),
    
]