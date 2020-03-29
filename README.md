# Whole Foods Delivery Slot Automated Script

Yes, amid COVID-19 trying to get Whole Foods delivery slots can get cumbersome. To free you off the constant hastle of checking for slots (and almost never finding one), this automated script can notify you (yes notifies you verbally, so you can go about your tasks) of when new delivery slots open.


## Usage:
The script works on **Chrome** for now. 
It initializes a Chrome webdriver, for which if you don't have one install it from: https://chromedriver.chromium.org/
You'll have to update the path of the this installed webdriver under: ```python driver = webdriver.Chrome()``` if its not the default location your OS needs. 

_The script works after you have added all the items to your cart! Note, have your cart ready before running this script! Also, please don't let your computer sleep._

### After you clone the project:
1. Run the requirements.txt (```python $ pip install -r requirements.txt```)
2. Run whole_foods_delivery_slot.py (```python $ python whole_foods_delivery_slot.py```)
3. Get a nice warm Tea, browse reddit, do something on Xbox, etc.
4. Once a slot opens the script will verbally notify you of an open slot.
5. Have fun! Stay Safe!
