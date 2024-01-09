
# coding: utf-8

# In[1]:


import csv
import requests
from bs4 import BeautifulSoup
import re
from haverhelpers import headless_selenium


# In[2]:


driver = headless_selenium()


# In[3]:


url = 'https://www.bmv.com.mx/'


# In[4]:


driver.get(url)


# In[5]:


bsobj = BeautifulSoup(driver.page_source, 'html.parser')

driver.quit()
# In[33]:


data = []
for li in bsobj.find('dl', {'id':'viewIPC'}).find_all('li'):
    field = li.text.strip().split(':')[0]
    value = li.find('span').text.strip()
    if field.lower() == 'date':
        data = [[field,value]] + data
    else:
        data.append([field,value])


# In[35]:


with open('IPC.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(data)

