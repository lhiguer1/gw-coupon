from time import sleep
import os
import secmail
import requests
import lxml.html
import random

COUPON_PATH = 'coupons'

ZIP_CODES = [ 
    85032, 85281, 85225, 85142, 85308, 85383, 85251, 85282, 85326, 85338, 85022,
    85345, 85204, 85301, 85255, 85008, 85201, 85205, 85351, 85248, 85374, 85207,
    85254, 85016, 85224, 85375, 85283, 85209, 85260, 85018, 85382, 85206, 85041, 
    85295, 85044, 85029, 85286, 85234, 85296, 85020, 85021, 85208, 85249, 85202,
    85015, 85226, 85027, 85212, 85379, 85051, 85086, 85210, 85033, 85302, 85042,
    85035, 85037, 85213, 85233, 85257, 85395, 85023, 85339, 85258, 85323, 85396, 
    85298, 85048, 85014, 85050, 85268, 85392, 85203, 85009, 85331, 85340, 85353, 
    85085, 85053, 85017, 85024, 85297, 85013, 85335, 85040, 85381, 85259, 85388, 
    85304, 85043, 85303, 85006, 85306, 85373, 85250, 85215, 85028, 85031, 85019, 
    85387, 85284, 85118, 85262, 85253, 85139, 85310, 85083, 85239, 85266, 85004, 
    85305, 85054, 85007, 85390, 85003, 85012, 85355, 85087, 85307, 85378, 85361, 
    85045, 85363, 85354, 85034, 85263, 85377, 85309, 85252, 85256, 85285, 85064, 
    85211, 85080, 85358, 85327, 85244, 85329, 85318, 85082, 85246, 85063, 85267, 
    85312, 85342, 85299, 85069, 85337, 85261, 85066, 85236, 85216, 85380, 85269, 
    85067, 85277, 85274, 85060, 85076, 85385, 85311, 85068, 85071, 85372, 85046, 
    85005, 85275, 85001, 85545, 85376, 85036, 85280, 85320, 85264, 85214, 85078, 
    85011, 85061, 85322, 85079, 85219, 85271, 85074, 85333, 85070, 85127, 85010, 
    85002, 85343, 85030, 85072, 85038, 85290, 85289, 85287, 85313, 85227, 85099, 
    85098, 85077, 85075, 85073, 85065, 85062, 85055, 85039, 85026, 85025, 85096, 
    85097, 85190
    ]

url = "https://goodwillaz.us10.list-manage.com/subscribe/post-json"
params = {
    "u": "8d92937eb473f959e4b574e25",
    "id": "c64256085e",
    "EMAIL": '',
    "MMERGE3": random.choice(ZIP_CODES),
    "subscribe": "Subscribe",
}

def get_links() -> dict:
    links = dict()

    # get email address
    sm = secmail.SecMail()
    links['email_address'] = sm.generate_email()
    
    # get confirmation link
    params['EMAIL'] = links['email_address']
    request = requests.get(url, params)
    if request.json()['result'] != 'success':
        return links 

    # wait for new email    
    for _ in range(10):
        sleep(60)
        messages = sm.get_messages(links['email_address'])
        if len(messages.json) == 1:
            break
    else:
        return links

    # find confirmation_email and respond
    confirmation_email = sm.read_message(links['email_address'], messages.json[0]['id'])

    tree = lxml.html.fromstring(confirmation_email.htmlBody)
    form_button = tree.find_class('formEmailButton')[0]
    links['confirmation'] = form_button.attrib.get('href')

    requests.get(links['confirmation'])

    # wait for second email which cointains link to coupon
    for _ in range(10):
        sleep(90)
        messages = sm.get_messages(links['email_address'])
        if len(messages.json) == 2:
            break
    else:
        return links

    ## find coupon link
    coupon_message = sm.read_message(links['email_address'], messages.json[0]['id'])
    tree = lxml.html.fromstring(coupon_message.htmlBody)

    for element in tree.iter(tag='img'):
        if element.attrib.get('alt') and 'Click here' in element.attrib.get('alt'):
            parent_element = element.getparent()
            break

    links['coupon'] = parent_element.attrib.get('href')
    return links

def save_links(links=None):
    links = links or get_links()

    if not os.path.exists(COUPON_PATH):
        os.mkdir(COUPON_PATH)

    path = os.path.join(COUPON_PATH, 'links.txt')
    with open(path, 'wt') as fd:
        fd.writelines('\n'.join([f'{link}={links[link]}' for link in links]))


def get_coupons(links=None) -> dict:
    links = links or get_links()

    if 'coupon' not in links.keys():
        return None
    
    request = requests.get(links['coupon'])
    tree = lxml.html.fromstring(request.text)
    
    coupon_elements = []
    for element in tree.iter(tag='h3'):
        if len(element.attrib) == 1:
            coupon_elements.append(element)

    coupons = {}
    for element in coupon_elements:
        month = element.text
        coupon_link = element.getnext().get('href')

        request = requests.get(coupon_link)
        coupons[month] = request.content

    return coupons

def save_coupons(coupons=None):
    coupons = coupons or get_coupons()
    if coupons is None:
        return

    if not os.path.exists(COUPON_PATH):
        os.mkdir(COUPON_PATH)

    for month in coupons:
        path = os.path.join(COUPON_PATH, month.lower()+'.png')
        with open(path, 'wb') as fd:
            fd.write(coupons[month])


if __name__=='__main__':
    links = get_links()
    save_links(links)
    coupons = get_coupons(links)
    save_coupons(coupons)
    