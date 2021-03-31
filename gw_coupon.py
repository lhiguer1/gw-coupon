from selenium import webdriver
from random import random
from time import sleep
from dotenv import dotenv_values
from tempMail2 import TempMail
from hashlib import md5
import requests
import pickle
import lxml.html
import os


def send_keys(driver, element, msg):
    '''Send msg to element. sleep() and random() are used to look more human'''
    sleep(random())
    for char in msg:
        sleep(random())
        element.send_keys(char)

def save_mailbox(mailbox):
    '''Save mailbox using pickle module along with the html of each email'''
    mailbox_path = 'mailbox'
    
    if not os.path.exists(mailbox_path):
        os.mkdir(mailbox_path)
    
    # save mailbox.pickle
    with open(os.path.join(mailbox_path, 'mailbox.pickle'), 'wb') as fp:
        pickle.dump(mailbox, fp)

    # save html of each email
    for i, email in enumerate(mailbox):
        html = email['mail_text_only']
        with open(os.path.join(mailbox_path, f'email{i}.html'), 'w') as fp:
            fp.write(html)



dotenv_config = dotenv_values()

# Phase 1: Get temp-mail email
tm = TempMail(api_key=dotenv_config.get('API_KEY'), api_domain=dotenv_config.get('API_DOMAIN'))
email_address = tm.get_email_address()
print(f'{email_address=}')

# Phase 2: Sign up to newsletter
driver = webdriver.Firefox(executable_path=os.path.relpath('webdrivers\geckodriver.exe'))
driver.get(dotenv_config.get('URL'))

element = driver.find_element_by_id('mce-EMAIL')
send_keys(driver, element, email_address)

element = driver.find_element_by_id('mce-FNAME')
send_keys(driver, element, dotenv_config.get('FNAME'))

element = driver.find_element_by_id('mce-LNAME')
send_keys(driver, element, dotenv_config.get('LNAME'))

element = driver.find_element_by_id('mce-MMERGE3')
send_keys(driver, element, dotenv_config.get('ZIP_CODE'))

element = driver.find_element_by_id('mc-embedded-subscribe')
sleep(2)
element.click()
sleep(1)
driver.close()
# Phase 3: Confirm email
## wait for email
for _ in range(5):
    sleep(5)
    mailbox = tm.get_mailbox(email_address, md5(email_address.encode()).hexdigest())
    if type(mailbox) == list and len(mailbox) == 1:
        break
else:
    raise Exception('Aborting Process: Mailbox not receiving any new emails.')

## save email and mailbox
save_mailbox(mailbox)

## find confirmation link and respond
confirmation_email = mailbox[0]['mail_text_only']

tree = lxml.html.fromstring(confirmation_email)
for link in tree.iterlinks():
    (element, attribute, confirmation_link, pos) = link
    if element.find_class('formEmailButton'):
        break
print(f'{confirmation_link=}')
requests.get(confirmation_link)

# Phase 4: Download coupon
## wait for second email which cointains link to coupon
sleep(20) # this one takes a while
for _ in range(5):
    sleep(10)
    mailbox = tm.get_mailbox(email_address, md5(email_address.encode()).hexdigest())
    if type(mailbox) == list and len(mailbox) == 2:
        break
else:
    raise Exception('Aborting Process: Mailbox not receiving any new emails.')

## save email and mailbox
save_mailbox(mailbox)

## find coupon link and respond
    