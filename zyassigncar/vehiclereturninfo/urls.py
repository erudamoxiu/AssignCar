from django.conf.urls import url
from .import views

urlpatterns = [
    url(r'^createVehicleReturn$', views.createVehicleReturn),
    url(r'^getVehicleReturn$', views.getVehicleReturn),
    url(r'^getAllVehicleReturn$', views.getAllVehicleReturn),
    url(r'^updateVehicleReturn$', views.updateVehicleReturn),
    url(r'^show_all_apply$', views.show_all_apply),
    url(r'^show_assign$', views.show_assign),
    url(r'^approval$', views.show_approval_vchiclereturn),
    url(r'^in_approval$', views.approval_vchiclereturn),
    url(r'^driver_data_all$', views.driver_data_all),
    url(r'^query_history$', views.query_history),
]
