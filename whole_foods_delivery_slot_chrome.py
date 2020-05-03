import bs4

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import sys
import time
import os


def getWFSlot(productUrl):
   headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
   }

   chrome_options = Options()
   chrome_options.add_argument("user-data-dir=_chrcache")
   driver = webdriver.Chrome(chrome_options=chrome_options)
   driver.get(productUrl)           
   html = driver.page_source
   soup = bs4.BeautifulSoup(html, "html.parser")
   time.sleep(60)
   no_open_slots = True

   while no_open_slots:
      driver.refresh()
      print("refreshed")
      html = driver.page_source
      soup = bs4.BeautifulSoup(html, "html.parser")
      time.sleep(4)

      try:
         slot_opened_text = "Not available"
         all_dates = soup.findAll("div", {"class": "ufss-date-select-toggle-text-availability"})
         for each_date in all_dates:
            if slot_opened_text not in each_date.text:
               print('SLOTS OPEN 2!')
               os.system('say "Slots for delivery opened!"')
               no_open_slots = False
               time.sleep(1400)
      except AttributeError:
         pass

      try:
         no_slot_pattern = 'No delivery windows available. New windows are released throughout the day.'
         if no_slot_pattern == soup.find('h4', class_ ='a-alert-heading').text:
            print("NO SLOTS!")
      except AttributeError: 
            print('SLOTS OPEN 3!')
            os.system('say "Slots for delivery opened!"')
            no_open_slots = False


      slot_patterns = ['Next available', '1-hour delivery windows', '2-hour delivery windows']
      try:
         next_slot_text = str([x.text for x in soup.findAll('h4', class_ ='ufss-slotgroup-heading-text a-text-normal')])
         if any(next_slot_text in slot_pattern for slot_pattern in slot_patterns):
            print('SLOTS OPEN!')
            winsound.Beep(freq, duration)
            no_open_slots = False

            autoCheckout(driver)
            
      except AttributeError:
         pass


getWFSlot('https://www.amazon.com/gp/buy/shipoptionselect/handlers/display.html?hasWorkingJavascript=1')


