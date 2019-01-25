from django.conf.urls import url

from .import views

urlpatterns = [
    url(r'^createdateDestFee$', views.createdateDestFee),
    url(r'^updateDestFee$',views.updateDestFee),
    url(r'^deleteDestFee$',views.deleteDestFee),
    url(r'^getAllDestFee$',views.getAllDestFee),
    url(r'^getDestFee$',views.getDestFee),
    url(r'^excel_upload$', views.excel_upload),
    url(r'^dest_fee$', views.dest_fee),
  ]