from django.conf.urls import url

from .import views

urlpatterns = [
    url(r'^createdateCarInfo$', views.createdateCarInfo),
    url(r'^updateCarInfo$',views.updateCarInfo),
    url(r'^deleteCarInfo$',views.deleteCarInfo),
    url(r'^getAllCarInfo$',views.getAllCarInfo),
    url(r'^getCarInfo$',views.getCarInfo),
    url(r'^excel_upload$',views.excel_upload),
    url(r'^car_info$',views.car_info),
  ]