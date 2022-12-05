#!/usr/bin/env python3

from libs.variables import ciscoips
from os import popen
from libs.variables import username, password, enable_secret, tmp_folder
from libs.functions import check_credentials_and_path, get_cdp_neighbors, write_descr

check_credentials_and_path(username, password, enable_secret, tmp_folder)

for ip in ciscoips:
    get_cdp_neighbors(ip, username, password, enable_secret, tmp_folder)
    ctfls = popen('cat temps/'+ip+' | grep / | wc -l').read()

    for i in range(1, int(ctfls)+1):
        descr = popen('cat temps/'+ip+' | grep -A 1 "bvim.lan" | awk \'NR%2{printf $0" ";next;}1\' | tail -n '+str(i)+' | awk -F\' \' \'BEGIN{OFS="-"} {print $1,$8,$9}\'').readline().strip()
        localint = popen('cat temps/'+ip+'| grep -A 1 "bvim.lan" | awk \'NR%2{printf $0" ";next;}1\' | tail -n '+str(i)+' | awk \'{print $2,$3}\'').readline().strip()
        write_descr(ip, username, password, enable_secret, localint, descr)
