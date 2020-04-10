- [Whole Foods and Amazon Fresh Delivery Slot Automated Script](#whole-foods-and-amazon-fresh-delivery-slot-automated-script)
  * [Usage:](#usage)
    + [Autobuy feature:](#autobuy-feature)
    + [After you clone the project:](#after-you-clone-the-project)
 - [Non-coding background help:](#non-coding-background-help)
 - [Visual Aid](#visual-aid)
 - [FAQ](#faq)
   * [Say is not a recognized command](#say-is-not-a-recognized-command)

# Whole Foods and Amazon Fresh Delivery Slot Automated Script

Yes, amid COVID-19 trying to get Whole Foods and Amazon Fresh delivery slots can get cumbersome. To free you off the constant hassle of checking for slots (and almost never finding one), this automated script can notify you (yes notifies you verbally, so you can go about your tasks) of when new delivery slots open.


## Usage:
Supports **MacOS, Linux, and Windows**.

The script works on **Chrome** (```whole_foods_delivery_slot_chrome.py``` for Whole Foods) (```amazon_fresh_delivery_slot_chrome.py``` for Amazon Fresh) and **FireFox** (```whole_foods_delivery_slot_firefox.py```) for now. This does not support "Autobuy feature".

Note, use the ```whole_foods_delivery_windows.py``` for Windows. Also, only for this OS, you'll have to install an additional package ```winsound```

### Autobuy feature:

If you'd like the script to select the first available time, and proceed all the way through checkout, please use the ```whole_foods_delivery_autobuy.py```. 
 
It initializes a  webdriver, for which if you don't have one install it from: https://chromedriver.chromium.org/ for Chrome and https://github.com/mozilla/geckodriver/releases for FireFox.

You'll have to update the path of the this installed webdriver under: ```python driver = webdriver.Chrome()``` if its not the default location your OS needs. Similarly, for FireFox ```python driver = webdriver.Firefox(executable_path="<your-webdriver-path>")```

Script was written on Python 2.7.10




_The script works after you have added all the items to your cart! Note, have your cart ready before running this script! Also, please don't let your computer sleep. Let your computer do the work, while you sleep_



### After you clone the project:
_Walkthrough for Chrome for Whole Foods, follow same steps if running on FireFox with the FireFox script_

1. Run the requirements.txt (```$ pip install -r requirements.txt```)
2. Run whole_foods_delivery_slot_chrome.py (``` $ python whole_foods_delivery_slot_chrome.py```)
3. The first time you run this script, Whole Foods cart will ask you to login. After you login, go to the "Shipping and Payment" window. Its titled: _Schedule your order_. Leave the script running.
4. Get a nice warm Tea, browse reddit, do something on Xbox, etc.
5. Once a slot opens the script will verbally notify you of an open slot.
6. Proceed to checkout once you select a time slot. Stay Safe!

# Non-coding background help:
For people with no background with coding there is this [amazing post out there](https://www.notion.so/using-pcomputo-s-script-to-find-whole-foods-delivery-slots-acbb6d71ef934da7b6822b1df451a11c). 

_Note, I haven't written this blog, but I'd like to thank the person (don't who they are) who wrote it._

# Visual Aid

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

# FAQ
## say is not a recognized command
If say is not native to your OS. Please try using winsound. Comment/delete the code in the script that has `os.system('say...')` and incorporate the following snippet:

`import winsound`

`duration = 1000`

`freq = 440`

~~os.system('say ...')~~

`winsound.Beep(freq, duration)`

As an example, you can look at any of the Windows scripts. Also, there are certain issues in this repository revolving around this issue that have been solved. Please feel to check them out too.



