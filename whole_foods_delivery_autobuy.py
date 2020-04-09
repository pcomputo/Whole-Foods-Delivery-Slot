import bs4

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import sys
import time
import os


def autoCheckout(driver):
   driver = driver
   #wait = WebDriverWait(driver,8)
   #slot_select_comtinue = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[1]/div[4]/div[2]/div/div[3]/div/div/ul/li/span/span/div/div[2]/span/span/button')))
   #slot_select_continue = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[1]/div[4]/div[2]/div/div[3]/div/div/ul/li/span/span/div/div[2]/span/span/button')))
   time.sleep(1)
   try:
      slot_select_button = driver.find_element_by_xpath('/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[1]/div[4]/div[2]/div/div[3]/div/div/ul/li/span/span/div/div[2]/span/span/button')
      slot_select_button.click()
      print("Clicked open slot")
   except NoSuchElementException:
      slot_select_button = driver.find_element_by_xpath('/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[1]/div[4]/div[2]/div/div[4]/div/div/ul/li/span/span/div/div[2]/span/span/button')
      slot_select_button.click()

   slot_continue_button = driver.find_element_by_xpath('/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div[3]/div/span/span/span/input')
   slot_continue_button.click()
   print("Selected slot and continued to next page")

   #slot_select_continue = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[1]/div[4]/div[2]/div/div[3]/div/div/ul/li/span/span/div/div[2]/span/span/button')))
   #slot_select_continue.click()
   
   try:
      outofstock_select_continue = driver.find_element_by_xpath('/html/body/div[5]/div/form/div[25]/div/div/span/span/input')
      outofstock_select_continue.click()
      print("Passed out of stock")
   except NoSuchElementException:
      pass

   try:
      time.sleep(6)
      payment_select_continue = driver.find_element_by_xpath('/html/body/div[5]/div[1]/div[2]/div[2]/div[4]/div/form/div[3]/div[1]/div[2]/div/div/div/div[1]/span/span/input')
      payment_select_continue.click()
      print("Payment method selected")


      time.sleep(6)
      try:
         review_select_continue = driver.find_element_by_xpath('/html/body/div[5]/div[1]/div[2]/form/div/div/div/div[2]/div/div[1]/div/div[1]/div/span/span/input')
         review_select_continue.click()
         print("Order reviewed")
      except NoSuchElementException:
         review_select_continue = driver.find_element_by_xpath('/html/body/div[5]/div[1]/div[2]/form/div/div/div/div[2]/div[2]/div/div[1]/span/span/input')
         review_select_continue.click()
         print("Order reviewed")

      print("Order Placed!")
      os.system('say "Order Placed!"')
   except NoSuchElementException:
      print("Found a slot but it got taken, run script again.")
      os.system('say "Found a slot but it got taken, run script again."')
      time.sleep(1400)

def getWFSlot(productUrl):
   headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
   }

   driver = webdriver.Chrome()
   driver.get(productUrl)
   driver.maximize_window()         
   html = driver.page_source
   soup = bs4.BeautifulSoup(html, "html.parser")
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
            os.system('say "Slots for delivery opened!"')
            no_open_slots = False

            autoCheckout(driver)
            
      except AttributeError:
         pass

      try:
         slot_opened_text = "Not available"
         all_dates = soup.findAll("div", {"class": "ufss-date-select-toggle-text-availability"})
         for each_date in all_dates:
            if slot_opened_text not in each_date.text:
               print('SLOTS OPEN!')
               os.system('say "Slots for delivery opened!"')
               no_open_slots = False
               autoCheckout(driver)

      except AttributeError:
         pass

      try:
         no_slot_pattern = 'No delivery windows available. New windows are released throughout the day.'
         if no_slot_pattern == soup.find('h4', class_ ='a-alert-heading').text:
            print("NO SLOTS!")
      except AttributeError: 
            print('SLOTS OPEN!')
            os.system('say "Slots for delivery opened!"')
            no_open_slots = False

            autoCheckout(driver)


getWFSlot('https://www.amazon.com/gp/buy/shipoptionselect/handlers/display.html?hasWorkingJavascript=1')


