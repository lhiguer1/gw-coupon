from selenium import webdriver
from random import random
from time import sleep
from dotenv import dotenv_values
from tempMail2 import TempMail
import os


def send_keys(driver, element, msg):
    '''Send msg to element. sleep() and random() are used to look more human'''
    sleep(random())
    for char in msg:
        sleep(random())
        element.send_keys(char)

dotenv_config = dotenv_values()

# Phase 1: Get temp-mail email
# Phase 2: Sign up to newsletter
email = "johnsmith@email.com"
driver = webdriver.Firefox(executable_path=os.path.relpath('webdrivers\geckodriver.exe'))
driver.get(dotenv_config.get('URL'))

element = driver.find_element_by_id('mce-EMAIL')
send_keys(driver, element, email)

element = driver.find_element_by_id('mce-FNAME')
send_keys(driver, element, dotenv_config.get('FNAME'))

element = driver.find_element_by_id('mce-LNAME')
send_keys(driver, element, dotenv_config.get('LNAME'))

element = driver.find_element_by_id('mce-MMERGE3')
send_keys(driver, element, dotenv_config.get('ZIP_CODE'))

element = driver.find_element_by_id('mc-embedded-subscribe')
element.click()

# Phase 3: Confirm email
# Phase 4: Download coupon
