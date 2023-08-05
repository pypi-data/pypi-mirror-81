import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlencode


"""
Example usage:

from pythonthaibulksms.thaibulksms import thaibulksms_sms

thaibulksms_sms(
    'YOUR_USERNAME',
    'YOUR_PASSWORD',
    '0899999999', # recipient phone number
    'Hello! How are you?', # message
    True,  # True = corporate, False = standard
    sender='MY COMPANY', # optional, needs to be set up in advance with thaibulksms.com
    schedule='2009301116', # optional, format YYMMDDhhmm
)
"""
def thaibulksms_sms(username, password, msisdn, message, corporate, sender=None, schedule=None):
    # required parameters
    data = {
        'username': username,
        'password': password,
        'msisdn': msisdn,
        'message': message,
        'force': 'premium' if corporate else 'standard'
    }
    #
    # optional parameters
    if schedule:
        data['ScheduledDelivery'] = schedule
    if sender:
        data['sender'] = sender
    #
    # call api
    return thaibulksms_api('https://www.thaibulksms.com/sms_api.php', data)

# todo: add thaibulksms_requestotp

# todo: add thaibulksms_verifyotp

def thaibulksms_api(url, data, format_response=True):
    r = requests.post(
        url,
        data=urlencode(data),
        headers={
            'accept': 'application/xml',
            'content-type': 'application/x-www-form-urlencoded'
        }
    )

    # extract data from response
    if format_response:
        root = ET.ElementTree(ET.fromstring(r.text)).getroot()
        response = []

        # sms api
        if root.tag.lower() == 'sms':
            for queue in root:
                contents = {}
                for el in queue.iter():
                    tag = el.tag.lower()
                    if tag in ['detail', 'msisdn', 'transaction']:
                        contents[tag] = el.text
                    elif tag in ['status', 'usedcredit', 'remaincredit']:
                        contents[tag] = int(el.text)
                response.append(contents)

        # otp api (todo)
        #
        #

    if not format_response:
        response = r.text

    # return
    return {
        'status': r.status_code,
        'response': response
    }