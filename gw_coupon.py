from time import sleep
from dotenv import dotenv_values
import secmail
import requests
import lxml.html
import os
import re

# dotenv setup
dotenv_config = dotenv_values()
zip_code = dotenv_config.get('ZIP_CODE')

# Phase 1: Get secmail email
sm = secmail.SecMail()
email_address = sm.generate_email()
print(f'{email_address=}')

# Phase 2: Sign up to newsletter
url = "https://goodwillaz.us10.list-manage.com/subscribe/post-json"
params = {
    "u": "8d92937eb473f959e4b574e25",
    "id": "c64256085e",
    "EMAIL": email_address,
    "MMERGE3": zip_code,
    "subscribe": "Subscribe",
}

request = requests.get(url, params)
assert request.json()['result'] == 'success'

# Phase 3: Confirm email
for _ in range(5):
    sleep(30)
    messages = sm.get_messages(email_address)
    if len(messages.json) == 1:
        break
else:
    raise Exception('Aborting Process: Mailbox not receiving any new emails.')

## find confirmation link and respond
confirmation_email = sm.read_message(email_address, messages.json[0]['id'])

tree = lxml.html.fromstring(confirmation_email.htmlBody)
form_button = tree.find_class('formEmailButton')[0]
confirmation_link = form_button.attrib.get('href')

print(f'{confirmation_link=}')
requests.get(confirmation_link)

# Phase 4: Download coupon
## wait for second email which cointains link to coupon
for _ in range(5):
    sleep(90)
    messages = sm.get_messages(email_address)
    if len(messages.json) == 2:
        break
else:
    raise Exception('Aborting Process: Mailbox not receiving any new emails.')

## find coupon link and Download
coupon_message = sm.read_message(email_address, messages.json[0]['id'])
tree = lxml.html.fromstring(coupon_message.htmlBody)

for element in tree.iter(tag='img'):
    if element.attrib.get('alt') and 'Click here' in element.attrib.get('alt'):
        parent_element = element.getparent()
        coupon_link = parent_element.attrib.get('href')
        break
    
print(f'{coupon_link=}')
