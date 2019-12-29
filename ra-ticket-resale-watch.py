import lxml
import os
import requests as re
import time
from lxml import html
from tabulate import tabulate
from datetime import datetime
from twilio.rest import Client

account_sid = os.environ["TWILIO_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
twilio_number = os.environ["TWILIO_NUMBER"]
my_number = os.environ["MY_NUMBER"]
raurl = input("\nfull Resident Advisor URL \n")

twilio_text_count = 0

while twilio_text_count < 3:
    print("date:")
    print(datetime.now())
    print("\nchecking tickets for:\n" + raurl + "\n")

    print("sending http request:")
    response = re.get(raurl)
    print(response)

    tree = lxml.html.fromstring(response.text)
    ticket_classes = tree.xpath('//*[@id="tickets"]/ul/li/@class')
    offsale_types = tree.xpath('//*[@id="tickets"]/ul/li/p/text()')
    offsale_prices = tree.xpath('//*[@id="tickets"]/ul/li/p/span/text()')
    onsale_types = tree.xpath('//*[@id="tickets"]/ul/li/label/p/text()')
    onsale_prices = tree.xpath('//*[@id="tickets"]/ul/li/label/p/span/text()')
    event_title = tree.xpath('//div/h1')[0].text
    event_day = tree.xpath('//main/ul/li/section/div/div/div/aside/ul/li/text()')[0]
    event_date = tree.xpath('//main/ul/li/section/div/div/div/aside/ul/li/a/text()')[0]
    event_time = tree.xpath('//main/ul/li/section/div/div/div/aside/ul/li/text()')[1]
    event_location = tree.xpath('//*[@id="detail"]/ul/li[2]/a[1]/text()')[0]

    print("\nevent title: \n" + event_title)
    print("\ndate: \n" + event_day + "\n" + event_date + "\n" + event_time)
    print("\nlocation:\n" + event_location)
    print(f"\nThere are {len(offsale_types)} ticket types off sale")
    print(f"There are {len(onsale_types)} ticket types on sale")

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
        
        print("\ngo buy them quick\n" + raurl + "\n")
        
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body = "ticket available: " + raurl,
            from_= twilio_number,
            to = my_number
        )
        
        print("twilio message id:")
        print(message.sid)
        print("\n")
        
    elif len(onsale_types) == 0:
        print("twilio text count:")
        print(twilio_text_count)
        print("\nnothing on sale :( ... retrying in 5 min\n")
        time.sleep(300)

print("script paused at " + str(datetime.now()) + " due to twilio text count being reached! Please restart")
