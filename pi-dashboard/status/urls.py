from django.urls import path

from . import views


app_name = 'status'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('devices/', views.devices, name='devices'),
    path('device/<int:device_num>/', views.device, name='device')
]
