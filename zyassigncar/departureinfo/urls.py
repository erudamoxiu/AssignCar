from django.conf.urls import url

from .import views

urlpatterns = [
    url(r'^createdateDeparture$', views.createdateDeparture),
    url(r'^updateDeparture$', views.updateDeparture),
    url(r'^deleteDeparture$', views.deleteDeparture),
    url(r'^getAllDeparture$', views.getAllDeparture),
    url(r'^getDeparture$', views.getDeparture),
    url(r'^excel_upload$', views.excel_upload),
    url(r'^departureinfo$', views.departure_info),
  ]