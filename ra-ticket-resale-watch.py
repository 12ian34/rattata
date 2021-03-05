import lxml
import os
import requests as re
import time
from lxml import html
from tabulate import tabulate
from datetime import datetime
from twilio.rest import Client

TWILIO_SID = os.environ["TWILIO_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_NUMBER = os.environ["TWILIO_NUMBER"]
MY_NUMBER = os.environ["MY_NUMBER"]
twilio_text_count = 0
url_ra = input("\nfull Resident Advisor URL \n")
url_embedtickets = url_ra.strip("/").replace("events", "widget/event") + "/embedtickets"

def parse_url(url):
    print("date:")
    print(datetime.now())
    print("\nchecking tickets for:\n" + url + "\n")
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    print("sending http request:")
    response = re.get(url, headers=headers)
    tree = lxml.html.fromstring(response.text)
    print(response)
    return tree

while twilio_text_count < 3:
    tree = parse_url(url_embedtickets)
    ticket_classes = tree.xpath('//*[@id="ticket-types"]/ul[@data-ticket-info-selector-id="tickets-info"]/li/@class')
    offsale_types = tree.xpath('//*[@id="ticket-types"]/ul[@data-ticket-info-selector-id="tickets-info"]/li[@class="closed"]/div/div[@class="type-title"]/text()')
    offsale_prices = tree.xpath('//*[@id="ticket-types"]/ul[@data-ticket-info-selector-id="tickets-info"]/li[@class="closed"]/div/div[@class="type-price"]/text()')
    #test below with multiple currently onsale tickets
    onsale_types = tree.xpath('//*[@id="ticket-types"]/ul[@data-ticket-info-selector-id="tickets-info"]/li[@class="onsale but"]/label/div[@class="pr8"]/text()')
    onsale_prices = tree.xpath('//*[@id="ticket-types"]/ul[@data-ticket-info-selector-id="tickets-info"]/li[@class="onsale but"]/label/div[@class="type-price"]/text()')
    
    if len(offsale_types) > 0:
        print("\nthe following tickets are off sale: \n")
        headers = ['ticket', 'price']
        table = zip(offsale_types, offsale_prices)
        print(tabulate(table, headers=headers, floatfmt=".4f"))

    if len(onsale_types) > 0:
        print("\n\nthe following tickets are on sale: \n")
        headers = ['ticket', 'price']
        table = zip(onsale_types, onsale_prices)
        print(tabulate(table, headers=headers, floatfmt=".4f") + "\n")
        twilio_text_count += 1
        print("\ntwilio text count:")
        print(twilio_text_count)
        print("\ngo buy them quick\n" + url_ra + "\n")
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body = "ticket available: " + url_ra,
            from_= TWILIO_NUMBER,
            to = MY_NUMBER
        )
        print("twilio message id:")
        print(message.sid)
        print("\n")
        time.sleep(3600)

    elif len(onsale_types) == 0:
        print("\ntwilio text count:")
        print(twilio_text_count)
        print("\nnothing on sale :( ... retrying in 5 min\n")
        time.sleep(180)

print("script paused at " + str(datetime.now()) + " due to twilio text count being reached! Please manually restart")
