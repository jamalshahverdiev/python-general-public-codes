#!/usr/bin/env python3
 
from flask import Flask
app = Flask(__name__)
socket_file = '/run/haproxy/admin.sock'
