
def send_email(SMTP, smtp_server_domain, user, pwd, sender, receiver, message):
    server = SMTP(smtp_server_domain, 25)
    server.set_debuglevel(1)
    server.ehlo(smtp_server_domain)
    server.esmtp_features['auth'] = 'LOGIN'
    server.login(user, pwd)
    server.sendmail(sender, receiver, message)
    server.close()
    print('Successfully sent the mail')