from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url('^accounts/', include('django.contrib.auth.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^transactions/$', views.transactions, name='transactions'),
    url(r'^clothing/$', views.clothing, name='clothing'),
    url(r'^accessory/$', views.accessory, name='accessory'),    
]