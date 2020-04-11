import bs4

from selenium import webdriver

import sys
import time

import winsound


def getWFSlot(productUrl):
   driver = webdriver.Chrome()
   driver.get(productUrl)           
   html = driver.page_source
   soup = bs4.BeautifulSoup(html)
   time.sleep(60)
   no_open_slots = True
        
   duration = 1000
   freq = 440

   while no_open_slots:
      driver.refresh()
      print("refreshed")
      html = driver.page_source
      soup = bs4.BeautifulSoup(html)
      time.sleep(4)

      slot_pattern = 'Next available'
      try:
         next_slot_text = str([x.text for x in soup.findAll('h4', class_ ='ufss-slotgroup-heading-text a-text-normal')])
         if slot_pattern in next_slot_text:
            print('SLOTS OPEN!')
            winsound.Beep(freq, duration)
            no_open_slots = False
            time.sleep(1400)
      except AttributeError:
         continue

      try:
         no_slot_pattern = 'No delivery windows available. New windows are released throughout the day.'
         if no_slot_pattern in [x.text for x in soup.findAll('h4', class_ ='a-alert-heading')]:
            print("NO SLOTS!")
      except AttributeError: 
            print('SLOTS OPEN!')
            winsound.Beep(freq, duration)
            no_open_slots = False


getWFSlot('https://www.amazon.com/gp/buy/shipoptionselect/handlers/display.html?hasWorkingJavascript=1')


