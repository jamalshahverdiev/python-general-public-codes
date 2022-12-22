#!/usr/bin/env python3

from smtplib import SMTP
from src.variables import sender_email, sender_password, receiver_email, message
from src.functions import send_email

send_email(SMTP, sender_email, sender_password, receiver_email, message)

