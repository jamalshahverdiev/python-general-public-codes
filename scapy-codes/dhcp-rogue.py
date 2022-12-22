#!/usr/bin/env python3

from logging import getLogger, ERROR
getLogger("scapy.runtime").setLevel(ERROR)
from scapy.all import sendp, sniff
from src.dhcproguevars import dhcp_request
from src.functions import dhcp_get_offer
# Only send the DHCP request in the channel layer(L2)
sendp(dhcp_request)

# Sniff for any DHCP packets and don't store them in the memory
sniff(prn=dhcp_get_offer, store=0)
