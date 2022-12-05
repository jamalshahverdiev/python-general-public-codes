from os import getcwd
from paramiko import SSHClient, AutoAddPolicy

codepath = getcwd()
static_macs_file='/StaticMacs'
ip_file='iplist'
outputdir = codepath+'/outdir/'
frommail = "from.email@gmail.com"
fromemailpass = "from.email.password"
tomail= "to.email@gmail.com"
ssh = SSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())