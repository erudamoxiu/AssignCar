from django.conf.urls import url

from .import views

urlpatterns = [
    url(r'^createdateDriver$', views.createdateDriver),
    url(r'^updateDriver$', views.updateDriver),
    url(r'^deleteDriver$', views.deleteDriver),
    url(r'^getAllDriver$', views.getAllDriver),
    url(r'^getDriver$', views.getDriver),
    url(r'^excel_upload$', views.excel_upload),
    url(r'^driver$', views.driver),

  ]