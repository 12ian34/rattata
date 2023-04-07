import os
import sys
import time
from datetime import datetime

import inquirer
import lxml
import requests as re
from lxml import html
from tabulate import tabulate
from twilio.rest import Client

TWILIO_SID = os.environ["TWILIO_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_NUMBER = os.environ["TWILIO_NUMBER"]
MY_NUMBER = os.environ["MY_NUMBER"]
twilio_text_count = 0

print(sys.argv)
if len(sys.argv) > 2:
    print('you have provided too many arguments! just run the script without an argument and you will be prompted for the URL to track, otherwise, pass the URL as one argument e.g.\n python ra-ticket-resale-watch.py https://ra.co/events/1432652')

if len(sys.argv) == 2:
    url_ra = sys.argv[1]

if len(sys.argv) < 2:
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

def get_tickets(tree):
    ticket_classes = tree.xpath('//*[@id="ticket-types"]/ul[@data-ticket-info-selector-id="tickets-info"]/li/@class')
    offsale_types = tree.xpath('//*[@id="ticket-types"]/ul[@data-ticket-info-selector-id="tickets-info"]/li[@class="closed"]/div/div[@class="type-title"]/text()')
    offsale_prices = tree.xpath('//*[@id="ticket-types"]/ul[@data-ticket-info-selector-id="tickets-info"]/li[@class="closed"]/div/div[@class="type-price"]/text()')
    #test below with multiple currently onsale tickets
    onsale_types = tree.xpath('//*[@id="ticket-types"]/ul[@data-ticket-info-selector-id="tickets-info"]/li[@class="onsale but"]/label/div[@class="pr8"]/text()')
    onsale_prices = tree.xpath('//*[@id="ticket-types"]/ul[@data-ticket-info-selector-id="tickets-info"]/li[@class="onsale but"]/label/div[@class="type-price"]/text()')
    return(
        ticket_classes,
        offsale_types,
        offsale_prices,
        onsale_types,
        onsale_prices,
    )

def choose_ticket(offsale_types, onsale_types):
    question = [inquirer.Checkbox('ticket', message="Select the ticket(s) you'd like from the list below and then press Enter. Your current selection is", choices=offsale_types + onsale_types)]
    answer = inquirer.prompt(question)
    return answer

def show_tickets(offsale_types, onsale_types):
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

def check_tickets(answer, onsale_types):
    for ticket_type in answer['ticket']:
        if ticket_type in onsale_types:
            return True
    return False
 
def send_text():
    global twilio_text_count
    print("\nyour tickets are available! go buy them quick\n" + url_ra + "\n")
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body = "ticket available! : " + url_ra,
        from_= TWILIO_NUMBER,
        to = MY_NUMBER)
    twilio_text_count += 1
    print("twilio message id:")
    print(message.sid)
    print("\n")
    return twilio_text_count

(ticket_classes,
 offsale_types,
 offsale_prices,
 onsale_types,
 onsale_prices,
) = get_tickets(parse_url(url_embedtickets))
show_tickets(offsale_types, onsale_types)
answer = choose_ticket(offsale_types, onsale_types)
twilio_text_count = 0

while twilio_text_count < 3:
    get_tickets(parse_url(url_embedtickets))
    if check_tickets(answer, onsale_types) == True:
        send_text()
        print('\nchecking again in one hour ...')
        time.sleep(3600)
    elif check_tickets(answer, onsale_types) == False:
        print('\nyour chosen ticket is still not on sale :( ... retrying in 3 min\n')
        time.sleep(60)

print("script paused at " + str(datetime.now()) + " because we've already sent you 2 texts! Please manually restart")

