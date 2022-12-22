
def send_email(SMTP, sender_email, sender_password, receiver_email, message):
    server = SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email , message)
    server.quit()

def printer_func(site, dollar, euro):
    return "%s saytindan istinad edilmishdir: " % str(site), "1 USD = %s AZN" % str(dollar), "1 EURO: %s AZN" % str(euro)