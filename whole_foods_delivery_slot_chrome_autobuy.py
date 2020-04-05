import sys
import time
import os
import requests
import json
import config

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twilio.rest import Client

def send_ifttt():
    
    report = {}
    report["value1"] = "Amazon order placed"
    requests.post(config.ifttt_webhook, data=report)


def send_sms():
    client = Client(config.twilio['account_sid'], config.twilio['auth_token'])

    message = client.messages \
                    .create(
                        body="Amazon order placed!",
                        from_=config.twilio['twilio_number'],
                        to=config.twilio['cell_number']
                    )

    print(message.sid)

def send_slack_notification():

    wekbook_url = config.slack['webhook']

    data = {
        'text': 'Amazon order has been placed!',
        'username': config.slack['username'],
        'icon_emoji': ':robot_face:'
    }

    response = requests.post(wekbook_url, data=json.dumps(
        data), headers={'Content-Type': 'application/json'})
    return response

def getWFSlot(productUrl):
    # set refresh interval
    interval = 4

    # create webdriver object and fetch URL
    chrome_options = Options()
    # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(productUrl)
    
    no_open_slots = True

    # loop while no open slots found
    while no_open_slots:

        # loop while URL is not on the delivery window page
        while driver.current_url != productUrl:
            print(f"Not on delivery window page. Waiting {interval} seconds to check again...")
            time.sleep(interval)
        
        try:
            # search for delivery slot buttons, select first one, then click continue
            slot_button = driver.find_elements_by_xpath("//button[@class='a-button-text ufss-slot-toggle-native-button']")[0]
            slot_button.click()
            continue_button = driver.find_elements_by_xpath("//input[@class='a-button-input' and @type='submit']")[0]
            continue_button.click()

            # play alert sound if p
            os.system('say "Time slots available. Completing purchase."')

            # click continue if intermediate purchase window shows up
            try:        
                top_continue_button = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
                    (By.XPATH, "//input[@class='a-button-text ' and @type='submit']")
                    ))
                top_continue_button.click()
            except:
                print("intermediate page not loaded, checking for purchase button")

            # place order
            try:        
                place_order_button = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
                    (By.XPATH, "//input[@class='a-button-text place-your-order-button']")
                    ))
                # place_order_button.click()
                print("Order placed!")

                # send notifications
                send_slack_notification()
                send_sms()
                send_ifttt()

                # sleep for an hour after success then quit
                time.sleep(3600)
                driver.quit()
                exit(0)
            except:
                # if error, sleep for an hour
                print("Error occured, cannot place order.")      
                time.sleep(3600)     
            
        except IndexError:
            # if no slots found, do nothing
            print(f"No slots found, waiting {interval} seconds...", end = "")

        # refresh the page, update soup object, wait specified time before next check
        time.sleep(interval)
        driver.refresh()
        print("refreshing.")

getWFSlot('https://www.amazon.com/gp/buy/shipoptionselect/handlers/display.html?hasWorkingJavascript=1')

