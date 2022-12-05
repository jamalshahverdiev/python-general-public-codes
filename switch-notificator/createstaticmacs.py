#!/usr/bin/env python3
from os import system
from sys import argv, exit
from lib.functions import *
from lib.variables import ip_file, static_macs_file, codepath

if len(argv) < 4:
    exit('Usage: {} switchusername switchpassword vlanID'.format(argv[0]))
else:
    pass

with open(ip_file, 'r') as iplist:
    for ip in iplist.readlines():
        ssh.connect(''.join(ip.split()), port=22, username=argv[1], password=argv[2], look_for_keys=False, allow_agent=False)
        macget(argv[3], ''.join(ip.split()))
        getallMACs(''.join(ip.split()), argv[3])

with open(outputdir+'/MAC.list', 'r') as dirtymacs:
    for line in dirtymacs.readlines():
        with open(static_macs_file, 'a') as macresult:
            with open(codepath+static_macs_file) as smacs:
                if line in smacs:
                    print('This line is exists in the StaticMacs file!!!')
                else:
                    macresult.write(line)
                    print('New line is written to the StaticMacs file!!!')
    system('rm -rf '+outputdir+'/*')

ssh.close()

