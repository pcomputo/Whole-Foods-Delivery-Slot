from bs4 import BeautifulSoup
import bs4

import requests
import urllib

from selenium import webdriver


import json


import sys
import time

import re
import os

'''
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebPage
'''


def getAmazonPrice(productUrl):
   headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
   }

   driver = webdriver.Chrome()
   driver.get(productUrl)           
   html = driver.page_source
   soup = bs4.BeautifulSoup(html)
   time.sleep(50)   
   while 100:
   	driver.refresh()
   	print("refreshed")
   	html = driver.page_source
   	soup = bs4.BeautifulSoup(html)
   	time.sleep(10)
   	pattern = 'No delivery windows available. New windows are released throughout the day.'
   	if pattern == soup.find('h4', class_ ='a-alert-heading').text:
   		mydivs = soup.find_all("div", class_ = "a-box a-alert a-alert-info ufss-slotselect-unavailable-alert")
   		if mydivs:
   			print("NO SLOTS!")
   		else:
   			print("SLOTS OPEN!")
   	else:
   		os.system('say "Slots for delivery opened!"')
   	#print(mydivs)
   	''''
   	for foo in soup.find_all('div', attrs={'class': 'ufss-widget-grid'}):

   		#print(foo)
   		
   		foo_descendants = foo.descendants
   		for d in foo_descendants:
   		#print(d)
   		 #if d.name == 'div' and d.get('class', '') == ['a-row']:
   		 for poo in soup.find_all('div', attrs={'class': 'a-row ufss-widget-grid-row'}):
   		 	poo_descendants = poo.descendants
   		 	print("poo",poo.descendants)
   		 	for p in poo_descendants:
   		 		print(p)
   		 		if p.name == 'div' and p.get('class', '') == ['a-column a-span10 a-span-last']:
   		 		 print("NO SLOTS")
   		 		 print()
   		 	#print("NO SLOTS!")
   		 	#print(d.text)
   		 	'''

price = getAmazonPrice('https://www.amazon.com/gp/buy/shipoptionselect/handlers/display.html?hasWorkingJavascript=1')
print(price)

