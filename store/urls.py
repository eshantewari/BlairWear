from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url('^accounts/', include('django.contrib.auth.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^transactions/$', views.transactions, name='transactions'),
    url(r'^clothing/$', views.clothing, name='clothing'),
    url(r'^accessory/$', views.accessory, name='accessory'),
    url(r'^choose_dates/$', views.choose_dates, name='choose_dates'),
    url(r'^delete_transaction/$', views.delete_transaction, name='delete_transaction'),
    url(r'^confirmation/$', views.confirmation, name='confirmation'),
    url(r'^inventory/$', views.inventory, name='inventory'),
    url(r'^not_authorized/$', views.not_authorized, name='not_authorized'),
]
