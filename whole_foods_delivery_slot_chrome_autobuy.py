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
    requests.post(config.ifttt['webhook'], data=report)


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
            print(f"Not on delivery window page. Waiting {config.interval} seconds to check again...")
            time.sleep(config.interval)
        
        try:
            time.sleep(1) # wait 1 second for page to fully load     
            
            # search for delivery slot buttons, select first one, then click continue
            if driver.find_elements_by_xpath("//button[@class='a-button-text ufss-slot-toggle-native-button']"):
                try:
                    slot_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                        (By.XPATH, "//button[@class='a-button-text ufss-slot-toggle-native-button']")
                        ))
                    slot_button.click()
 
                    os.system('say "Time slot found. Completing purchase."')
                except:
                    print("slot button not clickable")
                    continue
                
                try:
                    continue_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                        (By.XPATH, "//input[@class='a-button-input' and @type='submit']")
                        ))
                    continue_button.click()
                except:
                    print("continue button not clickable")
                    continue

            else:
                # if no slots found, wait specified interval before refreshing page and restarting loop
                print(f"No slots found, waiting {config.interval} seconds...", end = "")
                time.sleep(config.interval)
                driver.refresh()
                print("refreshing.")
                continue

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
                # time.sleep(1) # wait 1 second for page to fully load     
                place_order_button = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
                    (By.XPATH, "//input[@class='a-button-text place-your-order-button']")
                    ))
                if config.enable_purchase:
                    place_order_button.click()
                    print("Order placed!")

                    # send notifications
                    if config.notifications['slack']:
                        print('sending slack notification')
                        send_slack_notification()
                    if config.notifications['twilio_sms']:
                        print('sending sms notification')
                        send_sms()
                    if config.notifications['ifttt']:
                        print('sending ifttt notification')
                        send_ifttt()
                else:
                    print("Purchasing disabled. Please complete purchase manually.")


                # sleep for an hour after success then quit
                time.sleep(3600)
                driver.quit()
                exit(0)
            except:
                # if error, sleep for an hour
                print("Error occured, cannot place order.")      
                time.sleep(3600)     
            
        except:
            print("Uncaught exception in main loop. Cannot continue.")

getWFSlot('https://www.amazon.com/gp/buy/shipoptionselect/handlers/display.html?hasWorkingJavascript=1')

