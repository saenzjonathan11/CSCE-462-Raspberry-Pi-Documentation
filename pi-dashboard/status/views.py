from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

posts = [
    {
        'hostname': 'dummylocalhost',
        'ip4_address': '127.0.0.1',
        'ip6_address': '0:0:0:0:0:0:0:1',
        'mac_address': '05:32:E3:01:CC:D4',
        'bandw_in': '50',
        'bandw_out': '40',
        'bandw_total': '90',
        'last_seen': 'Mon 06 Apr 2020 02:49:45 AM CDT'
    },
    {
        'hostname': 'dummyhost1',
        'ip4_address': '165.231.210.187',
        'ip6_address': '0:0:0:0:0:ffff:a5e7:d2bb',
        'mac_address': '4D:E6:13:C8:70:46',
        'bandw_in': '25',
        'bandw_out': '15',
        'bandw_total': '40',
        'last_seen': 'Mon 04 Apr 2020 8:49:45 AM CDT'
    },
    {
        'hostname': 'dummyhost2',
        'ip4_address': '52.96.68.234',
        'ip6_address': '0:0:0:0:0:ffff:3460:44ea',
        'mac_address': '1A:87:D0:D3:62:D0',
        'bandw_in': '20',
        'bandw_out': '10',
        'bandw_total': '30',
        'last_seen': 'Mon 02 Apr 2020 3:49:45 AM CDT'
    },
    {
        'hostname': 'dummyhost3',
        'ip4_address': '241.85.20.252',
        'ip6_address': '0:0:0:0:0:ffff:f155:14fc',
        'mac_address': '8B:99:5E:5A:2D:8E',
        'bandw_in': '32',
        'bandw_out': '18',
        'bandw_total': '50',
        'last_seen': 'Mon 01 Apr 2020 12:49:45 PM CDT'
    },
    {
        'hostname': 'dummyhost4',
        'ip4_address': '161.101.136.39',
        'ip6_address': '0:0:0:0:0:ffff:a165:8827',
        'mac_address': '0D:04:99:54:0D:68',
        'bandw_in': '10',
        'bandw_out': '10',
        'bandw_total': '20',
        'last_seen': 'Mon 01 Apr 2020 10:49:45 AM CDT'
    }
]

def index(request):
    context = {
        'posts': posts
    }
    return render(request, 'status/index.html', context)

def about(request):
    return render(request, 'status/about.html')

def devices(request):
    context = {
        'posts': posts
    }
    return render(request, 'status/devices.html', context)

def device(request, device_num):
    response = "You're looking at the result of device %s."
    return HttpResponse(response % device_num) 
