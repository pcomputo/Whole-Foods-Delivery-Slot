import sys
import time
import os
import requests
import json
import config
import socket
import chromedriver_binary
import PySimpleGUI as sg

# from tkinter import messagebox
# import tkinter

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twilio.rest import Client

def prompt_for_config():
    # set theme for config window
    sg.theme('Dark')

    # set columns for each setting
    ifttt = [[sg.Text('IFTTT Webhook URL:'), sg.Input(key='ifttt_webhook')]]
    slack = [[sg.Text('Slack Webhook URL:'), sg.Input(key='slack_webhook')]]
    twilio = [
            [sg.Text('Twilio Account SID:'), sg.Input(key='twilio_account_sid')],
            [sg.Text('Twilio Auth Token:'), sg.Input(key='twilio_auth_token')],
            [sg.Text('Twilio Phone #:'), sg.Input(key='twilio_phone_number')],
            [sg.Text('Your Phone #:'), sg.Input(key='twilio_cell_number')]
            ]
    
    layout = [
        [sg.Text('Refresh interval:'), sg.Combo([5,10,30,60,300],60), sg.Text('seconds')],
        [sg.Checkbox('Enable Purchasing', default=True)],
        [sg.Checkbox('Enable IFTTT Notification', change_submits=True, enable_events=True, default='0', key="ifttt_enabled"),sg.Column(ifttt, key='ifttt_opts', visible=False)],
        [sg.Checkbox('Enable Slack Notification', change_submits=True, enable_events=True, default='0', key="slack_enabled"),sg.Column(slack, key='slack_opts', visible=False)],
        [sg.Checkbox('Enable Twilio SMS Notification', change_submits=True, enable_events=True, default='0', key="twilio_enabled"),sg.Column(twilio, key='twilio_opts', visible=False)]
        ]

    # draw window
    window = sg.Window('Configuration', layout)

    # process input into config window
    while True:  # Event Loop
        event, values = window.read()       # can also be written as event, values = window()
        print(event, values)
        if event is None or event == 'Quit':
            break
        if values['ifttt_enabled'] == True:
            window.FindElement('ifttt_opts').Update(visible=True)
        if values['ifttt_enabled'] == False:
            window.FindElement('ifttt_opts').Update(visible=False)
        if values['slack_enabled'] == True:
            window.FindElement('slack_opts').Update(visible=True)
        if values['slack_enabled'] == False:
            window.FindElement('slack_opts').Update(visible=False)
        if values['twilio_enabled'] == True:
            window.FindElement('twilio_opts').Update(visible=True)
        if values['twilio_enabled'] == False:
            window.FindElement('twilio_opts').Update(visible=False)

    window.close()


def send_ifttt():
    
    report = {}
    report["value1"] = "Whole Foods order has been placed!"
    requests.post(config.ifttt['webhook'], data=report)


def send_sms():
    client = Client(config.twilio['account_sid'], config.twilio['auth_token'])

    message = client.messages \
                    .create(
                        body="Whole Foods order has been placed!",
                        from_=config.twilio['twilio_number'],
                        to=config.twilio['cell_number']
                    )

    print(message.sid)


def send_slack_notification():

    wekbook_url = config.slack['webhook']

    data = {
        'text': 'Whole Foods order has been placed!',
        'username': config.slack['username'],
        'icon_emoji': ':robot_face:'
    }

    response = requests.post(wekbook_url, data=json.dumps(
        data), headers={'Content-Type': 'application/json'})
    return response


def show_message_box():
    sg.theme('Dark')  # please make your windows colorful
    
    alert_layout = [
            [sg.Text('Whole Foods purchase completed successfully!')],
            [sg.Submit()]
            ]

    alert_window = sg.Window('Whole Foods Purchase Successful', alert_layout)

    alert_window.read()
    alert_window.close()


def getWFSlot(productUrl):
    # create webdriver object
    chrome_options = Options()
    
    # create socket object
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # check to see if chrome is running in remote debugging mode
    location = ("127.0.0.1", 9222)
    result_of_check = a_socket.connect_ex(location)

    if result_of_check == 0:
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    # close socket object
    a_socket.close()

    # config webdriver and fetch product URL
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(productUrl)
    # driver.implicitly_wait(3)

    no_open_slots = True

    alternate_url = "https://www.amazon.com/gp/buy/itemselect/handlers/display.html?ie=UTF8&useCase=singleAddress&hasWorkingJavascript=1"

    # loop while no open slots found
    while no_open_slots:

        # loop while URL is not on the delivery window page
        while driver.current_url not in [productUrl, alternate_url]:
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
                except Exception as ex:
                    print("slot button not clickable")
                    print(repr(ex))
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

            # click continue if payment selection page shows up
            place_order_title = "Place Your Order - Amazon.com Checkout"
            select_payment_title = "Select a Payment Method - Amazon.com Checkout"

            WebDriverWait(driver, 10).until(lambda x: driver.title in [select_payment_title, place_order_title])

            if driver.title == select_payment_title:
                print("Payment selection page loaded, selecting default and continuing")
                try:
                    top_continue_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                        (By.XPATH, "//input[@class='a-button-text ' and @type='submit']")
                        ))
                    top_continue_button.click()
                except Exception as ex:
                    print(repr(ex))
            else:
                print("Payment selection page not loaded, proceeding with purchase")

            WebDriverWait(driver, 10).until(lambda x: driver.title == place_order_title)

            # place order
            if driver.title == place_order_title:
                try:
                    place_order_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
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
                        if config.notifications['message_box']:
                            print('displaying visual notification')
                            show_message_box()
                    else:
                        print("Purchasing disabled. Please complete purchase manually.")

                    # sleep for an hour after success then quit
                    time.sleep(3600)
                    driver.quit()
                    exit(0)
                except TimeoutError:
                    continue # retry loop if button doesn't appear for some reason
                except:
                    # if error, sleep for an hour in case the session can be manually recovered
                    print("The following exception occured, cannot place order.")
                    print(sys.exc_info()[0])
                    print(sys.exc_info()[1])
                    print(sys.exc_info()[2].tb_lineno)
                        
                    time.sleep(3600)     
            
        except:
            print("The following exception occured in the main loop. Cannot continue.")
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            print(sys.exc_info()[2].tb_lineno)     

if __name__ == "__main__":
    getWFSlot('https://www.amazon.com/gp/buy/shipoptionselect/handlers/display.html?hasWorkingJavascript=1')

