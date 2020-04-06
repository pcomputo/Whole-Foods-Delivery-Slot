import bs4

from selenium import webdriver

import sys
import time
import os
import pyttsx3

engine = pyttsx3.init() # object creation

def sayIt(textToSay):
   engine.say(textToSay)
   engine.runAndWait()

def getWFSlot(productUrl):
   headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
   }

   driver = webdriver.Chrome()
   driver.get(productUrl)           
   html = driver.page_source
   soup = bs4.BeautifulSoup(html)
   time.sleep(60)
   no_open_slots = True

   while no_open_slots:
      driver.refresh()
      print("refreshed")
      html = driver.page_source
      soup = bs4.BeautifulSoup(html)
      time.sleep(2)

      try:
         open_slots = soup.find('div', class_ ='orderSlotExists').text()
         if open_slots != "false":
            print('SLOTS OPEN!')
            sayIt("Slots for delivery opened!"
            no_open_slots = False
            time.sleep(1400)
      except AttributeError:
         continue


sayIt("Starting")
getWFSlot('https://www.amazon.com/gp/buy/shipoptionselect/handlers/display.html?hasWorkingJavascript=1')

engine.stop()
