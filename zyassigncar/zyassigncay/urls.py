"""zyassigncay URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'user/', include('user.urls')),
    url(r'factory/', include('factory.urls')),
    url(r'carmodel/', include('carmodel.urls')),
    url(r'departureinfo/', include('departureinfo.urls')),
    url(r'driver/', include('driver.urls')),
    url(r'destfee/', include('destfee.urls')),
    url(r'carinfo/', include('carinfo.urls')),
    url(r'assign/', include('assign.urls')),
    url(r'apply/', include('apply.urls')),
    url(r'vehiclereturninfo/', include('vehiclereturninfo.urls')),
]
