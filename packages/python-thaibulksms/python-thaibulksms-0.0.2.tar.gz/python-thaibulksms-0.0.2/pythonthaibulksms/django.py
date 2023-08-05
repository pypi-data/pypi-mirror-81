from django.conf import settings
from pythonthaibulksms.thaibulksms import thaibulksms_sms


"""
In your settings.py

THAIBULKSMS = {
    'default': {
        'username': 'YOUR_USERNAME',
        'password': 'YOUR_PASSWORD',
        'corporate': True,
        'sender': 'MY COMPANY' # optional, needs to be set up in advance with thaibulksms.com
    },
    'other_company': {
        'username': 'YOUR_OTHER_USERNAME',
        'password': 'YOUR_OTHER_PASSWORD',
        'corporate': True,
        'sender': 'MY OTHER COMPANY' # optional, needs to be set up in advance with thaibulksms.com
    }
}

Example usage:

from pythonthaibulksms.django import django_thaibulksms_sms

django_thaibulksms_sms(
    '0899999999', # recipient phone number
    'Hello! How are you?', # message
    'other_company', # optional, which config to use from your settings.py
    schedule='2009301116', # optional, format YYMMDDhhmm
)
"""

def django_thaibulksms_sms(msisdn, message, config='default', schedule=None):
    return thaibulksms_sms(
        settings.THAIBULKSMS[config]['username'],
        settings.THAIBULKSMS[config]['password'],
        msisdn,
        message,
        settings.THAIBULKSMS[config].get('corporate', False),
        sender=settings.THAIBULKSMS[config].get('sender', None),
        schedule=schedule
    )