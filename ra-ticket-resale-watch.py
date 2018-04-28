
# coding: utf-8

# In[516]:


# import necessary packages
import lxml
import requests as re
from lxml import html
from tabulate import tabulate


# In[518]:


# ask for full ra url
raurl = input("\nfull Resident Advisor URL \n")

# confirm url
print("\nchecking tickets for\n" + raurl + "\n")


# In[519]:


# send HTTP request and store response
print("sending http request\n")
response = re.get(raurl)
print(response)


# In[520]:


# parse xml tree
tree = lxml.html.fromstring(response.text)


# In[521]:


# extract and print event title
event_title = tree.xpath('//div/h1')[0].text
print("\nevent title: \n" + event_title)


# In[522]:


# extract and print event date
event_day = tree.xpath('//main/ul/li/section/div/div/div/aside/ul/li/text()')[0]
event_date = tree.xpath('//main/ul/li/section/div/div/div/aside/ul/li/a/text()')[0]
event_time = tree.xpath('//main/ul/li/section/div/div/div/aside/ul/li/text()')[1]
print("\ndate: \n" + event_day + "\n" + event_date + "\n" + event_time)


# In[523]:


# extract and print event location
event_location = tree.xpath('//*[@id="detail"]/ul/li[2]/a[1]/text()')[0]
print("\nlocation:\n" + event_location)


# In[524]:


# extract ticket class list, not used yet
ticket_classes = tree.xpath('//*[@id="tickets"]/ul/li/@class')


# In[525]:


# extract and print off sale ticket detail lists 
offsale_types = tree.xpath('//*[@id="tickets"]/ul/li/p/text()')
offsale_prices = tree.xpath('//*[@id="tickets"]/ul/li/p/span/text()')


# In[526]:


print("\nthe following tickets are off sale: \n")
headers = ['ticket', 'price']
table = zip(offsale_types, offsale_prices)
print(tabulate(table, headers=headers, floatfmt=".4f"))
print("\n ... one day ... \n")


# In[527]:


# extract and print on sale ticket detail lists 
onsale_types = tree.xpath('//*[@id="tickets"]/ul/li/label/p/text()')
onsale_prices = tree.xpath('//*[@id="tickets"]/ul/li/label/p/span/text()')


# In[529]:


# inform whether tickets are on sale, if so, print table and share link

if len(onsale_types)==0:
    print("\nnothing on sale:(\n")
else:
    print("the following tickets are on sale: \n")
    headers = ['ticket', 'price']
    table = zip(onsale_types, onsale_prices)
    print(tabulate(table, headers=headers, floatfmt=".4f"))
    print("\ngo buy them quick\n" + raurl)


# # old code

# In[530]:


#for idx, val in enumerate(ticket_classes):
#    print(idx, val)


# In[531]:


#for item in tree.xpath("//li"):
#    if "onsale but" in item.classes:
#        print("on sale")
#    else:
#        print("closed :(")

