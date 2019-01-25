from django.conf.urls import url
from user import views

urlpatterns = [
    url(r'^getUserInfo$', views.getUserInfo),
    url(r'^addUser$', views.addUser),
    url(r'^getUser$', views.getUser),
    url(r'^getJSAPI$', views.getJSAPI),
    url(r'^getUserDetail$', views.getUserDetail),
    url(r'^updateUser$', views.updateUser),
    url(r'^deleteUser$', views.deleteUser),
  ]