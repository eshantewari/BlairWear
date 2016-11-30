from django.conf.urls import url, include
from django.contrib.auth.views import password_change, password_change_done

from . import views

urlpatterns = [
    url(r'^accounts/password/change/$', password_change, {'post_change_redirect' : '/accounts/password/change/done/'},name="password_change"),
    url(r'^accounts/password/change/done/$',password_change_done),
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
