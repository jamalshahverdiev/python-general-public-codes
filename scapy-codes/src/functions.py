from scapy.all import DHCP, Ether, IP
# Define a callback function for when DHCP packets are received
def dhcp_get_offer(pkt):
    # Check if the DHCP packet is a DHCP offer from DHCP server
    if DHCP in pkt and pkt[DHCP].options[0][1] == 2:
        print('DHCP server IP address: {0} MAC address: {1}'.format(pkt[IP].src, pkt[Ether].src))