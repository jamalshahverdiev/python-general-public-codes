user = 'smtprelayuser'
pwd = 'Securep@$$'
sender = 'username@domain.az'
receiver = ['username@gmail.com']
subject = 'Test email from Sales'
body = 'Testing sending mail using exchange servers'
smtp_server_domain = 'mail.domain.az'
message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
""" % (sender, ", ".join(receiver), subject, body)
