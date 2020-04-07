# Whole Foods and Amazon Fresh Delivery Slot Automated Script

Yes, amid COVID-19 trying to get Whole Foods and Amazon Fresh delivery slots can get cumbersome. To free you off the constant hassle of checking for slots (and almost never finding one), this automated script can notify you (yes notifies you verbally, so you can go about your tasks) of when new delivery slots open. The autobuy script will automatically place your order using the first available delivery window.


## Description:
Supports **MacOS, Linux, and Windows**.

Note, use the ```whole_foods_delivery_windows.py``` for Windows. Also, only for this OS, you'll have to install an additional package ```winsound```

The script works on **Chrome** (```whole_foods_delivery_slot_chrome.py``` for Whole Foods), (```whole_foods_delivery_slot_chrome_autobuy.py``` for Whole Foods w/Automatic Purchase), (```amazon_fresh_delivery_slot_chrome.py``` for Amazon Fresh) and **FireFox** (```whole_foods_delivery_slot_firefox.py```) for now. 

Scripts were written on Python 2.7.10. whole_foods_delivery_slot_chrome_autobuy.py has been tested on Python 3.7.1


_The script works after you have added all the items to your cart! Note, have your cart ready before running this script! Also, please don't let your computer sleep. Let your computer do the work, while you sleep_


### Installation:

1. Clone the project into a local directory
2. Install the webdriver if you don't have it from: https://chromedriver.chromium.org/ for Chrome and https://github.com/mozilla/geckodriver/releases for FireFox.

You'll have to update the path of the this installed webdriver under: ```python driver = webdriver.Chrome()``` if its not the default location your OS needs. Similarly, for FireFox ```python driver = webdriver.Firefox(executable_path="<your-webdriver-path>")```
3. Run the requirements.txt (```$ pip install -r requirements.txt```)


### Usage:
_Walkthrough for Chrome for Whole Foods, follow same steps if running on FireFox with the FireFox script_

1. Run whole_foods_delivery_slot_chrome.py (``` $ python whole_foods_delivery_slot_chrome.py```)
2. The first time you run this script, Whole Foods cart will ask you to login. After you login, go to the "Shipping and Payment" window. Its titled: _Schedule your order_. Leave the script running.
3. Get a nice warm Tea, browse reddit, do something on Xbox, etc.
4. Once a slot opens the script will verbally notify you of an open slot.
5. Proceed to checkout once you select a time slot. Stay Safe!

> __Screen 1__
![alt text](https://github.com/pcomputo/Whole-Foods-Delivery-Slot/blob/master/instruction_img/step1.png)

> __Screen 2__
![alt text](https://github.com/pcomputo/Whole-Foods-Delivery-Slot/blob/master/instruction_img/step2.png)

> __Screen 3__
![alt text](https://github.com/pcomputo/Whole-Foods-Delivery-Slot/blob/master/instruction_img/step3.png)

> __Screen 4__
![alt text](https://github.com/pcomputo/Whole-Foods-Delivery-Slot/blob/master/instruction_img/step4.png)

> __Screen 5: Leave script running on this screen!__
![alt text](https://github.com/pcomputo/Whole-Foods-Delivery-Slot/blob/master/instruction_img/step5_new.png)

_Walkthrough for Chrome Autobuy script for Whole Foods_

Note: This script will AUTOMATICALLY complete your purchase with the first available delivery window
1. Copy config.py-example to config.py and update settings as necessary
2. Run whole_foods_delivery_slot_chrome_autobuy.py (``` $ python whole_foods_delivery_slot_chrome_autobuy.py```)
3. The first time you run this script, Whole Foods cart will ask you to login. After you login, go to the "Shipping and Payment" window. Its titled: _Schedule your order_. Leave the script running, it will automatically detect when you are on the right screen and will tell you that it's refreshing.
4. Get a nice warm Tea, browse reddit, do something on Xbox, etc.
5. Once a slot opens the script will verbally notify you of an open slot and complete the purchase using the first available slot. It will also optionally notify you via Slack, SMS or IFTTT
