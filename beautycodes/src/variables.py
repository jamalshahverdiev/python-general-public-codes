from requests import get
from bs4 import BeautifulSoup
from src.functions import printer_func

sender_email = "usdeurmezennesi@gmail.com"
sender_password = "D0llareur0"
receiver_email = "email.author@example.com"
finsurl='http://fins.az/bank'
response = get(finsurl)
respData = BeautifulSoup(response.content, "html.parser")
usd = respData.find('div', {'class': 'value'}).get_text()
eur = respData.find('div', {'class': 'value'}).find_next('div', {'class': 'value'}).get_text()
cbarurl='http://www.cbar.az/'
respcbar = get(cbarurl)
cbrespData = BeautifulSoup(respcbar.content, "html.parser")
cbusd = cbrespData.find('span', {'class': 'item item_4'}).get_text()
cbeur = cbrespData.find('span', {'class': 'item item_4'}).find_next('span', {'class': 'item item_4'}).get_text()
faz = printer_func(str(finsurl), str(usd), str(eur))
caz = printer_func(str(cbarurl), str(cbusd), str(cbeur))
message = """From: Euro Dollar <usdeurmezennesi@gmail.com>
To: Email Author <email.author@example.com>
Subject: Euro Dollar mezennesi

%s %s, %s
%s %s, %s
""" % (faz[0], faz[1], faz[2], caz[0], caz[1], caz[2])