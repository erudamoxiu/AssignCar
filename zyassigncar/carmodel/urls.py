from django.conf.urls import url

from .import views

urlpatterns = [
    url(r'^createdateCarModel$', views.createdateCarModel),
    url(r'^updateCarModel$', views.updateCarModel),
    url(r'^deleteCarModel$', views.deleteCarModel),
    url(r'^getAllCarModel$', views.getAllCarModel),
    url(r'^getCarModel$', views.getCarModel),
    url(r'^carmodel$', views.carmodel),
    url(r'^excel_upload$', views.excel_upload),

]