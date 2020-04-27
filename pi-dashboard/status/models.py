from django.db import models


class Device_Data(models.Model):
    hostname = models.CharField(max_length=100)
    ip4_address = models.CharField(max_length=15)
    ip6_address = models.CharField(max_length=39)
    mac_address = models.CharField(max_length=17)
    bandw_in = models.IntegerField(default=0)
    bandw_out = models.IntegerField(default=0)
    bandw_total = models.IntegerField(default=0)
    last_seen = models.CharField(max_length=40)