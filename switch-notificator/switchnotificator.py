#!/usr/bin/env python3
from os import system, path
from sys import exit, argv
from lib.functions import macget, filterMAC, emailsend
from lib.variables import ip_file, codepath, static_macs_file, frommail, fromemailpass, tomail, ssh, outputdir

if path.exists(codepath+static_macs_file) and path.getsize(codepath+static_macs_file) > 0:
    pass
else:
    print("File ", static_macs_file, " does not exists or empty!!!")
    print("To use switchnotificator.py script you must define static MAC address list in the ", static_macs_file, " file...")
    print("If you want define static mac list then, connect all your computers to you switch devices and use createstaticmacs.py script!!!")
    exit()

if len(argv) < 4:
    exit('Usage: {} switchusername switchpassword vlanID'.format(argv[0]))
else:
    pass

with open(ip_file, 'r') as iplist:
    for ip in iplist.readlines():
        ssh.connect(''.join(ip.split()), port=22, username=argv[1], password=argv[2], look_for_keys=False, allow_agent=False)
        macget(argv[3], ''.join(ip.split()))
        filterMAC(''.join(ip.split()), argv[3])

with open(outputdir+'/MAC.result', 'r') as macresult:
    for line in macresult.readlines():
        with open(codepath+static_macs_file) as smacs:
            if line in smacs:
                pass
            else:
                emailsend(frommail, fromemailpass, tomail, line.replace('\n', ''), argv[3])
                system('rm -rf '+outputdir+'/*')

ssh.close()
