from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^quotes$', views.quotes),
    url(r'^user/(?P<id>\d+)$', views.user),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^quotes/add$', views.add_quote),
    url(r'^like/(?P<id>\d+)$', views.like),
    url(r'^user/edit$', views.edit_user),
    url(r'^user/edit/(?P<id>\d+)$', views.edit),
    url(r'^quotes/destroy/(?P<id>\d+)$', views.destroy),
]