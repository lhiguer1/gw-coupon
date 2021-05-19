from time import sleep
from dotenv import dotenv_values
from tempMail2 import TempMail
from hashlib import md5
import requests
import pickle
import lxml.html
import os

# dotenv setup
dotenv_config = dotenv_values()
api_key = dotenv_config.get('API_KEY')
api_domain = dotenv_config.get('API_DOMAIN')
zip_code = dotenv_config.get('ZIP_CODE')

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


# Phase 1: Get temp-mail email
tm = TempMail(api_key=api_key, api_domain=api_domain)
email_address = tm.get_email_address()
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
    mailbox = tm.get_mailbox(email_address)
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
for _ in range(5):
    sleep(90)
    mailbox = tm.get_mailbox(email_address)
    if type(mailbox) == list and len(mailbox) == 2:
        break
else:
    raise Exception('Aborting Process: Mailbox not receiving any new emails.')

## save email and mailbox
save_mailbox(mailbox)

## find coupon link and Download
coupon_email = mailbox[1]['mail_text_only']

tree = lxml.html.fromstring(coupon_email)

for link in tree.iterlinks():
    (element, attribute, coupon_link, pos) = link

    if element.tag == 'img' and element.attrib.get('alt') != None and 'Click here' in element.attrib.get('alt'):
        parent_element = element.getparent()
        coupon_link = parent_element.attrib.get('href')
        break
    
print(f'{coupon_link=}')
