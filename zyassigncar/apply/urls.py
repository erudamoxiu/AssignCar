from django.conf.urls import url

from .import views

urlpatterns = {
    url(r'^createdateApply$', views.createdateApply),
    url(r'^updateApply$', views.updateApply),
    url(r'^deleteApply$', views.deleteApply),
    url(r'^getAllApply$', views.getAllApply),
    url(r'^getApply$', views.getApply),
    url(r'^createOrderNo$', views.createOrderNo),
    url(r'^approval_apply_all$', views.approval_apply_all),
    url(r'^approval_apply$', views.approval_apply),
    url(r'^approval_pass$', views.approval_pass_all),
}