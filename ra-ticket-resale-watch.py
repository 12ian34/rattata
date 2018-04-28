
# coding: utf-8

# In[454]:


# import necessary packages
import lxml
import requests as re
from lxml import html
from tabulate import tabulate


# In[455]:


# ask for full ra url
raurl = input("full Resident Advisor URL \n")

# confirm url
print("\nchecking tickets for\n" + raurl)


# In[456]:


# send HTTP request and store response
print("sending http request")
response = re.get(raurl)
print(response)


# In[457]:


tree = lxml.html.fromstring(response.text)


# In[458]:


event_title = tree.xpath('//div/h1')[0].text


# In[459]:


print("event title: \n" + event_title)


# In[460]:


event_day = tree.xpath('//main/ul/li/section/div/div/div/aside/ul/li/text()')[0]
event_date = tree.xpath('//main/ul/li/section/div/div/div/aside/ul/li/a/text()')[0]
event_time = tree.xpath('//main/ul/li/section/div/div/div/aside/ul/li/text()')[1]


# In[461]:


print("date: \n" + event_day + "\n" + event_date + "\n" + event_time)


# In[462]:


event_location = tree.xpath('//*[@id="detail"]/ul/li[2]/a[1]/text()')[0]


# In[463]:


print("location:\n" + event_location)


# In[464]:


ticket_classes = tree.xpath('//*[@id="tickets"]/ul/li/@class')


# In[466]:


offsale_types = tree.xpath('//*[@id="tickets"]/ul/li/p/text()')
offsale_prices = tree.xpath('//*[@id="tickets"]/ul/li/p/span/text()')


# In[467]:


print(offsale_types)


# In[468]:


print(offsale_prices)


# In[469]:


onsale_types = tree.xpath('//*[@id="tickets"]/ul/li/label/p/text()')
onsale_prices = tree.xpath('//*[@id="tickets"]/ul/li/label/p/span/text()')


# In[470]:


print(onsale_types)


# In[471]:


print(onsale_prices)


# In[472]:


if len(onsale_types)==0:
    print("nothing on sale:(")
else:
    print("the following tickets are on sale: \n \n")
    headers = ['ticket', 'price']
    table = zip(onsale_types, onsale_prices)
    print(tabulate(table, headers=headers, floatfmt=".4f"))
    print("\n \n go buy them quick " + raurl)


# In[473]:


#for idx, val in enumerate(ticket_classes):
#    print(idx, val)


# In[474]:


#for item in tree.xpath("//li"):
#    if "onsale but" in item.classes:
#        print("on sale")
#    else:
#        print("closed :(")

