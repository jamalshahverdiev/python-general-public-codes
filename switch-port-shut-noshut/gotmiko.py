#!/usr/bin/env python3
from sys import exit, argv
from netmiko import ConnectHandler

if len(argv) < 6:
    exit('Usage: {} username password enpass first_port_number second_port_number'.format(argv[0]))
else:
    pass

input_command = '{} {}'.format('show interfaces status | inc', argv[4])
output_command = '{} {}'.format('show interfaces status | inc', argv[4])
commandToNoShut = ['{} {}'.format('interface ', argv[5]), 'no shutdown']
commandToShut = ['{} {}'.format('interface ', argv[5]), 'shutdown']
user = argv[1]
password = argv[2]
enable_pass = argv[3]
devices_ip = ['192.168.20.80']

for ip in devices_ip:
    print('connection to device {}'.format(ip))
    device_params = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': user,
        'password': password,
        'secret': enable_pass
    }

    with ConnectHandler(**device_params) as ssh:
        ssh.enable()

        first_port = ssh.send_command(input_command)
        if "disabled" in first_port:
            result = ssh.send_config_set(commandToNoShut)
            print(result)
        elif "notconnect" in first_port:
            result = ssh.send_config_set(commandToShut)
            print(result)
