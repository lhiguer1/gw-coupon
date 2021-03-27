from selenium import webdriver
from random import random
from time import sleep
import os


def send_keys(driver, element, msg):
    '''Send msg to element. sleep() and random() are used to avoid getting blocked from the site'''
    sleep(random())
    for char in msg:
        sleep(random())
        element.send_keys(char)

# temporarily modify path
os.environ['path'] += os.pathsep + os.path.abspath('webdrivers')

driver = webdriver.Firefox()

driver.get('https://www.goodwillaz.org/coupons-store-specials/')

# Phase 1: Get temp-mail email
# Phase 2: Sign up to newsletter
email = "johnsmith@email.com"
first_name = "John"
last_name = "Smith"
zip_code = "1234"

element = driver.find_element_by_id('mce-EMAIL')
send_keys(driver, element, email)

element = driver.find_element_by_id('mce-FNAME')
send_keys(driver, element, first_name)

element = driver.find_element_by_id('mce-LNAME')
send_keys(driver, element, last_name)

element = driver.find_element_by_id('mce-MMERGE3')
send_keys(driver, element, zip_code)

element = driver.find_element_by_id('mc-embedded-subscribe')
element.click()

# Phase 3: Confirm email
# Phase 4: Download coupon
