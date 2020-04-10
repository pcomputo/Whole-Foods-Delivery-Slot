import bs4
import os
import sys
import time

from selenium import webdriver

# Initialize the driver
driver = webdriver.Chrome()
driver.get('https://www.amazon.com/gp/buy/shipoptionselect/handlers/display.html?hasWorkingJavascript=1')           

while True:
  # Load page HTML
  driver.refresh()
  html = driver.page_source
  soup = bs4.BeautifulSoup(html)

  # Iterate over the date windows
  for date_box in soup.findAll("div", {"class": "ufss-date-select-toggle-text-availability"}):

    # If anything but "Not available" appears, we assume a window is available
    if "Not available" not in date_box.text:
      print('Open slot! If it is not grabbed in 5 minutes we will continue searching...')
      os.system('say "Slots for delivery available!"')
      time.sleep(300)

  # Wait before trying again
  time.sleep(30)