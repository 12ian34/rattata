
# coding: utf-8

# In[489]:


# import necessary packages
import lxml
import requests as re
from lxml import html
from tabulate import tabulate


# In[490]:


# ask for full ra url
raurl = input("full Resident Advisor URL \n")

# confirm url
print("\nchecking tickets for\n" + raurl)


# In[491]:


# send HTTP request and store response
print("sending http request")
response = re.get(raurl)
print(response)


# In[492]:


# parse xml tree
tree = lxml.html.fromstring(response.text)


# In[493]:


# extract and print event title
event_title = tree.xpath('//div/h1')[0].text
print("event title: \n" + event_title)


# In[494]:


# extract and print event date
event_day = tree.xpath('//main/ul/li/section/div/div/div/aside/ul/li/text()')[0]
event_date = tree.xpath('//main/ul/li/section/div/div/div/aside/ul/li/a/text()')[0]
event_time = tree.xpath('//main/ul/li/section/div/div/div/aside/ul/li/text()')[1]
print("date: \n" + event_day + "\n" + event_date + "\n" + event_time)


# In[495]:


# extract and print event location
event_location = tree.xpath('//*[@id="detail"]/ul/li[2]/a[1]/text()')[0]
print("location:\n" + event_location)


# In[496]:


# extract ticket class list, not used yet
ticket_classes = tree.xpath('//*[@id="tickets"]/ul/li/@class')


# In[497]:


# extract and print off sale ticket detail lists 
offsale_types = tree.xpath('//*[@id="tickets"]/ul/li/p/text()')
offsale_prices = tree.xpath('//*[@id="tickets"]/ul/li/p/span/text()')


# In[498]:


print(offsale_types)


# In[499]:


print(offsale_prices)


# In[500]:


# extract and print on sale ticket detail lists 
onsale_types = tree.xpath('//*[@id="tickets"]/ul/li/label/p/text()')
onsale_prices = tree.xpath('//*[@id="tickets"]/ul/li/label/p/span/text()')


# In[501]:


print(onsale_types)


# In[502]:


print(onsale_prices)


# In[503]:


# inform whether tickets are on sale, if so, print table and share link

if len(onsale_types)==0:
    print("nothing on sale:(")
else:
    print("the following tickets are on sale: \n \n")
    headers = ['ticket', 'price']
    table = zip(onsale_types, onsale_prices)
    print(tabulate(table, headers=headers, floatfmt=".4f"))
    print("\n \n go buy them quick " + raurl)


# # old code

# In[504]:


#for idx, val in enumerate(ticket_classes):
#    print(idx, val)


# In[505]:


#for item in tree.xpath("//li"):
#    if "onsale but" in item.classes:
#        print("on sale")
#    else:
#        print("closed :(")

