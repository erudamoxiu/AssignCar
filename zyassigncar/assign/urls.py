from django.conf.urls import url

from .import views

urlpatterns = [
    url(r'^createAssign$', views.createAssign),
    url(r'^deleteAssign$',views.deleteAssign),
    url(r'^getAllAssign$',views.getAllAssign),
    url(r'^getAssign$',views.getAssign),

  ]