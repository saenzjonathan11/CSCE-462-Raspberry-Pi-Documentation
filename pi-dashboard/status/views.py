from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import os

hostap_status = os.popen('pidof hostapd | wc -l').readline()
cpu_temp = os.popen('vcgencmd measure_temp').readline()
mem_free = os.popen("free -m | awk '/Mem:/ {total=$2; used=$3} END { print used/total*100}'").readline()
#mem_free = os.popen("cat /proc/meminfo | awk 'FNR == 3 {free=$2}' END '{pring free/2000000*100}'").readline()
rx_packets = os.popen('cat /sys/class/net/wlan0/statistics/rx_packets').readline()
tx_packets = os.popen('cat /sys/class/net/wlan0/statistics/tx_packets').readline()
tx_bytes = os.popen('cat /sys/class/net/wlan0/statistics/tx_bytes').readline()
rx_bytes = os.popen('cat /sys/class/net/wlan0/statistics/rx_bytes').readline()
iw_wlan0 = os.popen('iw dev wlan0 info').readlines()
devices = os.popen('cat /var/lib/misc/dnsmasq.leases').readlines()


system_infos = [
        {
            'hostapStatus': hostap_status,
            'cpuTemp': cpu_temp,
            'memFree': mem_free,
            'rxPackets': rx_packets,
            'txPackets': tx_packets,
            'txBytes': tx_bytes,
            'rxBytes': rx_bytes,
            'nicInfo': iw_wlan0,
            'connectedDevices': devices
        }
]

posts = [
    {
        'hostname': 'dummylocalhost',
        'ip4_address': '127.0.0.1',
        'ip6_address': '0:0:0:0:0:0:0:1',
        'mac_address': '05:32:E3:01:CC:D4',
        'bandw_in': 12,
        'bandw_out': 30, 
        'bandw_total': 30,
        'last_seen': 'Mon 06 Apr 2020 02:49:45 AM CDT'
    }
]

def index(request):
    # interfacesList = [x.strip() for x in os.popen('ls /sys/class/net | grep -v lo').readlines()]
    interfacesList = [x.strip() for x in os.popen('ls /sys/class/net').readlines()]
    ifconfigOut = os.popen('ifconfig').readlines()
    tmpInterface = ""
    interfacesStrs = []
    for interface in ifconfigOut:
        if interface == '\n':
            interfacesStrs.append(tmpInterface)
            tmpInterface = ""
        else:
            tmpInterface += interface

    zipInterfaces = zip(interfacesList,interfacesStrs)

    context = {
        'posts': posts,
        'systemInfos': system_infos,
        'interfacesList': interfacesList,
        'zipInterfaces': zipInterfaces
        # 'interfacesStrs': interfacesStrs,
        # 'interfacesList': interfacesList
    }
    return render(request, 'status/index.html',context)
    #return render(request, 'status/index.html', context)

def dashboard(request):
    return render(request, 'status/dashboard.html')

def hotspot(request):

    
    return render(request, 'status/hotspot.html')




def interfaces(request):
    interfacesList = [x.strip() for x in os.popen('ls /sys/class/net').readlines()]
    ifconfigOut = os.popen('ifconfig').readlines()
    tmpInterface = ""
    interfacesStrs = []
    for interface in ifconfigOut:
        if interface == '\n':
            interfacesStrs.append(tmpInterface)
            tmpInterface = ""
        else:
            tmpInterface += interface

    zipInterfaces = zip(interfacesList,interfacesStrs)

    context = {
        'posts': posts,
        'systemInfos': system_infos,
        'interfacesList': interfacesList,
        'zipInterfaces': zipInterfaces
    }
    return render(request, 'status/interfaces.html', context)


def dhcp_dns(request):
    return render(request, 'status/dhcp_dns.html')

def authentication(request):
    return render(request, 'status/system.html')

def system(request):
    return render(request, 'status/system.html')

def about(request):
    return render(request, 'status/about.html')

def device(request, device_num):
    response = "You're looking at the result of device %s."
    return HttpResponse(response % device_num) 

def devices(request):
    context = {
        'posts': posts
    }
    return render(request, 'status/devices.html', context)

