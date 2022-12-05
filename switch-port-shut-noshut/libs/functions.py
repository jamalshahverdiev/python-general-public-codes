from netmiko import ConnectHandler
from libs.variables import config

def compare_ports_and_execute_command():
    for ip in [config.get('SWCREDS', 'IPS')]:
        print('connection to device {}'.format(ip))
        device_params = {
            'device_type': 'cisco_ios',
            'ip': ip,
            'username': config.get('SWCREDS', 'USERNAME'),
            'password': config.get('SWCREDS', 'PASSWORD'),
            'secret': config.get('SWCREDS', 'ENPASS')
        }

        with ConnectHandler(**device_params) as ssh:
            ssh.enable()

            first_port = ssh.send_command('{} {}'.format('show interfaces status | inc', config.get('SWCREDS', 'INPUT_PORT')))
            if "disabled" in first_port:
                result = ssh.send_config_set(['{} {}'.format('interface ', config.get('SWCREDS', 'OUTPUT_PORT')), 'no shutdown'])
                print(result)
            elif "notconnect" in first_port:
                result = ssh.send_config_set(['{} {}'.format('interface ', config.get('SWCREDS', 'OUTPUT_PORT')), 'shutdown'])
                print(result)
