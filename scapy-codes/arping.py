#!/usr/bin/env python3
# Don't forget: yum -y install tcpdump
from sys import exit, argv
from logging import getLogger, ERROR
getLogger("scapy.runtime").setLevel(ERROR)
from scapy.all import srp,Ether,ARP,conf

if len(argv) != 2:
    print("Usage: ./arping 192.168.1.0/24")
    exit(1)

conf.verb = 0
ans,unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=argv[1]), timeout=2)

print('   MAC Address       IP Address')
for snd,rcv in ans:
    print(rcv.sprintf("%Ether.src% | %ARP.psrc%"))
