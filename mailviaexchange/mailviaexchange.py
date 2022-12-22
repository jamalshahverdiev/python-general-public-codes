#!/usr/bin/env python3

from smtplib import SMTP
from src.functions import send_email
from src.variables import smtp_server_domain, user, pwd, sender, receiver, message

try:
    send_email(SMTP, smtp_server_domain, user, pwd, sender, receiver, message)
except:
    print('Failed to send mail')
