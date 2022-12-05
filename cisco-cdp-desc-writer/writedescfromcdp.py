#!/usr/bin/env python3

from netmiko import ConnectHandler
from getpass import getpass
from os import path, system, getcwd, popen
from sys import exit

ciscoips = ['172.16.100.50', '172.16.100.51', '172.16.100.52']

print("""
        Write CDP neighbor hostname and portid description to the local interface using SSH...
        Please enter needed credentials

        username: username used for the authentication
        password: password used for the authentication
        enable_secret: enable secret

        """)

username = input('Please enter username: ')
password = getpass('Please enter password for '+username+': ')
enable_secret = getpass('Please enter secret: ')

if username == "" or password == "" or enable_secret == "":
    print('username, password or enable_secret cannot be empty. Please enter valid credentials!!!')
    exit()

if path.isdir(getcwd()+'/temps/'):
    pass

else:
    print('The "temps" folder is not exists. Script will create automatically.')
    system('mkdir '+getcwd()+'/temps/')

def get_cdp_neighbors(ip, username, password, enable_secret):
    ssh_connection = ConnectHandler(
        device_type = 'cisco_ios',
        ip = ip,
        username = username,
        password = password,
        secret = enable_secret
    )
    ssh_connection.enable()
    result = ssh_connection.find_prompt() + "\n"
    result = ssh_connection.send_command("show cdp neighbors", delay_factor=0)

    with open(getcwd()+'/temps/'+ip, 'w') as outfile:
        outfile.write(result)
    ssh_connection.disconnect()

def write_descr(ip, username, password, enable_secret, localint, descr):
    ssh_connection = ConnectHandler(
        device_type = 'cisco_ios',
        ip = ip,
        username = username,
        password = password,
        secret = enable_secret
    )
    ssh_connection.enable()
    rt = ssh_connection.find_prompt() + "\n"
    rt = ssh_connection.send_command("conf t", delay_factor=0)
    rt = ssh_connection.send_command("int "+localint, delay_factor=0)
    rt = ssh_connection.send_command("description "+descr, delay_factor=0)
    ssh_connection.disconnect()

for ip in ciscoips:
    get_cdp_neighbors(ip, username, password, enable_secret)
    ctfls = popen('cat temps/'+ip+' | grep / | wc -l').read()

    for i in range(1, int(ctfls)+1):
        descr = popen('cat temps/'+ip+' | grep / | tail -n '+str(i)+' | awk -F\' \' \'BEGIN{OFS="-"} {print $1,$7,$8}\'').readline().strip()
        localint = popen('cat temps/'+ip+' | grep / | tail -n '+str(i)+' | awk \'{print $2,$3}\'').readline().strip()
        write_descr(ip, username, password, enable_secret, localint, descr)

