from django.urls import path

from . import views


app_name = 'status'

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.dashboard, name='dashboard'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    path('hotspot/', views.hotspot, name='hotspot'),
    path('interfaces/', views.interfaces, name='interfaces'),
    path('dhcp_dns/', views.dhcp_dns, name='dhcp_dns'),
    path('system/', views.system, name='system'),
    path('authentication/', views.authentication, name='authentication'),
    path('about/', views.about, name='about'),
    path('devices/', views.devices, name='devices'),
    path('device/<int:device_num>/', views.device, name='device')
]
