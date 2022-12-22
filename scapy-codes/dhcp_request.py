#!/usr/bin/env python3
from logging import getLogger, ERROR
getLogger("scapy.runtime").setLevel(ERROR)
from src.dhcprequestvars import pktboot, netcard
from scapy.all import srp1, DHCP
start = 2
end = 255

for i in range(start, end):
    srp1(
        pktboot/DHCP(
        options=[
            ("message-type","request"),
            ("server_id","10.0.0.1"),
            ("requested_addr",'10.0.0.'+str(i)+''),
            "end"
            ]
        ),
         timeout=2,
         iface=netcard
         )

