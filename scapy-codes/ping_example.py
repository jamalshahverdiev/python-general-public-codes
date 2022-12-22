#!/usr/bin/env python3
# Don't forget sniff traffic in the 10.50.94.100 server with the following command:
# tcpdump -n -e -A -i em0 host 10.50.63.228 and not port 22
from scapy.all import send, IP, ICMP, srloop
from src.variables import sher, source, ipadd
# ipadd = input('Please enter IP address to ping: ')

for i in range(1, 2):
    send(IP(src=source,dst="{0}".format(ipadd))/ICMP()/sher)
#srloop(IP(dst="{0}".format(ipadd))/ICMP(), count=4)
