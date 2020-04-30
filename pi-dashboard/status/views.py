from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import os
import re

hostap_status = os.popen('pidof hostapd | wc -l').readline()
cpu_temp = os.popen('vcgencmd measure_temp').readline()
mem_free = os.popen("free -m | awk '/Mem:/ {total=$2; used=$3} END { print used/total*100}'").readline()
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

wifiStandards = {
        'a': '802.11a - 5 GHz',
        'b': '802.11b - 2.4 GHz',
        'g': '802.11g - 2.4 GHz',
        'n': '802.11n - 2.4 GHz',
        'ac': '802.11.ac - 5 GHz'
        }

def index(request):
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
        'systemInfos': system_infos,
        'interfacesList': interfacesList,
        'zipInterfaces': zipInterfaces
    }
    return render(request, 'status/index.html',context)

def dashboard(request):
    devices = os.popen('arp -a').readlines()
    devicesLL = []
    i = 0

    for device in devices:
        deviceInfo = device.split(" ")
        if deviceInfo[0] != '?' and deviceInfo[3] != '<incomplete>' and deviceInfo[1] != '(1.1.1.1)':
            devicesLL.append({})
            devicesLL[i]["hostname"] = deviceInfo[0]
            devicesLL[i]["ip"] = deviceInfo[1][1:-1]
            devicesLL[i]["mac"] = deviceInfo[3].strip()
            i += 1
    context = {
        "devices": devicesLL
    }
    os.system("sudo vnstat -u -i wlan0")
    os.system("rm status/static/status/img/summary1.png")
    # os.system("rm status/static/status/img/summary2.png")
    os.system("rm status/static/status/img/summary3.png")
    os.system("vnstati -vs -c 1 -i wlan0 -o status/static/status/img/summary1.png")
    # os.system("vnstati -h -i wlan0 -o status/static/status/img/summary2.png")
    os.system("vnstati -s -i wlan0+eth0 -o status/static/status/img/summary3.png")

    return render(request, 'status/dashboard.html', context)

def hotspot(request):

    hostapdConf = [x.strip() for x in os.popen('cat /etc/hostapd/hostapd.conf').readlines()]

    ap_interface=""
    ap_ssid = ""
    ap_country_code = ""
    ap_channel = ""
    ap_passphrase = ""
    ap_hw_mode = ""

    for hostapdCon in hostapdConf:
        if (re.search('(?<=^interface=).*', hostapdCon)):
            ap_interface = re.search('(?<=^interface=).*', hostapdCon).group()
        if (re.search('(?<=^ssid=).*', hostapdCon)):
            ap_ssid = re.search('(?<=^ssid=).*', hostapdCon).group()
        if (re.search('(?<=^country_code=).*', hostapdCon)):
            ap_country_code = re.search('(?<=^country_code=).*', hostapdCon).group()
        if (re.search('(?<=^channel=).*', hostapdCon)):
            ap_channel = re.search('(?<=^channel=).*', hostapdCon).group()
        if (re.search('(?<=^wpa_passphrase=).*', hostapdCon)):
            ap_passphrase = re.search('(?<=^wpa_passphrase=).*', hostapdCon).group()
        if (re.search('(?<=^hw_mode=).*', hostapdCon)):
            ap_hw_mode = re.search('(?<=^hw_mode=).*', hostapdCon).group()

    context = {
        'apInterface': ap_interface,
        'apSSID': ap_ssid,
        'apChannel': ap_channel,
        'apPassphrase': ap_passphrase,
        'apHwMode': wifiStandards[ap_hw_mode],
        'apCountryCode': "US"
    }
    return render(request, 'status/hotspot.html',context)

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
        'systemInfos': system_infos,
        'interfacesList': interfacesList,
        'zipInterfaces': zipInterfaces
    }
    return render(request, 'status/interfaces.html', context)

def dhcp_dns(request):
    return render(request, 'status/dhcp_dns.html')

# def authentication(request):
#     return render(request, 'status/system.html')

def system(request):
    return render(request, 'status/system.html')

def about(request):
    return render(request, 'status/about.html')