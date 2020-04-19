import bs4

from selenium import webdriver

import sys
import time
import os
import winsound
import pyttsx3

engine = pyttsx3.init() # object creation

def sayIt(textToSay):
   engine.say(textToSay)
   engine.runAndWait()

def getWFSlot(productUrl):
   driver = webdriver.Firefox()
#   driver = webdriver.Firefox(executable_path=r"C:\Users\jason\Downloads\geckodriver-v0.26.0-win64\geckodriver.exe")
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
      time.sleep(4)

      slot_patterns = ['Next available', '1-hour delivery windows', '2-hour delivery windows']
      try:
         next_slot_text = soup.find('h4', class_ ='ufss-slotgroup-heading-text a-text-normal').text
         if any(next_slot_text in slot_pattern for slot_pattern in slot_patterns):
            print('SLOTS OPEN!')
            sayIt("Slots for delivery opened!")
            no_open_slots = False
            time.sleep(1400)
      except AttributeError:
         pass

      try:
         slot_opened_text = "Not available"
         all_dates = soup.findAll("div", {"class": "ufss-date-select-toggle-text-availability"})
         for each_date in all_dates:
            if slot_opened_text not in each_date.text:
               print('SLOTS OPEN!')
               sayIt("Slots for delivery opened!")
               no_open_slots = False
               time.sleep(1400)
      except AttributeError:
         pass

      try:
         no_slot_pattern = 'No delivery windows available. New windows are released throughout the day.'
         if no_slot_pattern == soup.find('h4', class_ ='a-alert-heading').text:
            print("NO SLOTS!")
      except AttributeError: 
            print('SLOTS OPEN!')
            sayIt("Slots for delivery opened!")
            no_open_slots = False

sayIt("Starting")
getWFSlot('https://www.amazon.com/gp/buy/shipoptionselect/handlers/display.html?hasWorkingJavascript=1')

engine.stop()
