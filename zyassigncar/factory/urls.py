from django.conf.urls import url

from .import views

urlpatterns = [
    url(r'^createdateFactory$', views.createdateFactory),
    url(r'^updateFactory$', views.updateFactory),
    url(r'^deleteFactory$', views.deleteFactory),
    url(r'^getAllFactory$', views.getAllFactory),
    url(r'^getFactory$', views.getFactory),
    url(r'^excel_upload$', views.excel_upload),
    url(r'^factory$', views.factory),
  ]