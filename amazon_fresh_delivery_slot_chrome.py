import bs4

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

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

      no_open_slots = "No doorstep delivery windows are available for"
      try:
         no_slots_from_web = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/div/div/form/div[3]/div[4]/div/div[2]/div[2]/div[6]/div/div[2]/div/div[2]/div/div[20]/div[1]/div[1]/div/div/div/span').text
         if no_open_slots in no_slots_from_web:
            pass
         else:
            print('SLOTS OPEN!')
            sayIt("Slots for delivery opened!")
            no_open_slots = False
            time.sleep(1400)
      except NoSuchElementException:
         print('SLOTS OPEN!')
         sayIt("Slots for delivery opened!")
         no_open_slots = False
         time.sleep(1400)


      try:
         open_slots = soup.find('div', class_ ='orderSlotExists').text()
         if open_slots != "false":
            print('SLOTS OPEN!')
            sayIt("Slots for delivery opened!")
            no_open_slots = False
            time.sleep(1400)
      except AttributeError:
         pass

      

      


sayIt("Starting")
getWFSlot('https://www.amazon.com/gp/buy/shipoptionselect/handlers/display.html?hasWorkingJavascript=1')

engine.stop()
