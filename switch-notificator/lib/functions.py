from smtplib import SMTP
from os import system
from lib.variables import ssh, outputdir

def emailsend(frommail, fromemailpass, tomail, mac, vlanID):
    message =  """From: From Email <{2}>
To: To Email <{3}>
Subject: New MAC address for VLAN {1}
MAC address "{0}" is not founded in "StaticMacs" file""".format(mac, vlanID, frommail, tomail)
    server = SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(frommail, fromemailpass)
    server.sendmail(frommail, tomail, message)
    server.quit()

def macget(vlanID, ip):
    stdin, stdout, stderr = ssh.exec_command('show mac address-table vlan '+vlanID+'')
    output = stdout.readlines()

    with open(outputdir+''+ip+'', 'wb') as switchout:
        switchout.write(''.join(output))

def filterMAC(ip, vlanID):
    system('cat '+outputdir+'/'+ip+' | grep -v -i ALL | grep '+vlanID+' | awk \'{print $2 }\' >> '+outputdir+'/MAC.result')

def getallMACs(ip, vlanID):
    system('cat '+outputdir+'/'+ip+' | grep -v -i ALL | grep '+vlanID+' | awk \'{print $2 }\' >> '+outputdir+'/MAC.list')

