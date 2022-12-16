#!/usr/bin/env python3

from socket import socket, AF_UNIX, SOCK_STREAM
from flask import make_response, request
from functools import wraps

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == 'haproxy' and auth.password == 'haproxy':
            return f(*args, **kwargs)

        return make_response('Login and password required!', 400, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

    return decorated

def filter_cicd(f):
    @wraps(f)
    def wrapped(*args, **kwargs):

        with open('access_list.txt', 'r') as filehandle:
            filecontents = filehandle.readlines()
            API_ALLOWED_IPS = list(map(lambda x:x.strip(),filecontents))

        for IP in API_ALLOWED_IPS:
            if str(request.remote_addr).startswith(IP) or str(request.remote_addr) == IP:
                return f(*args, **kwargs)
        return 'Your IP Is Not allowed ' + request.remote_addr
    return wrapped

def executeCommand(commandToSend, socket_file):
    socket_open = socket(AF_UNIX, SOCK_STREAM)
    socket_open.settimeout(1)
    socket_open.connect(socket_file)
    socket_open.send(str.encode(commandToSend))
    file_handle = socket_open.makefile()
    data = file_handle.read().splitlines()
    socket_open.close()
    return '\n'.join(data)

