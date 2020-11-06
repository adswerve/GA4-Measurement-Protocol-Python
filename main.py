import requests
import sys
import json
import retrying
from ga4measurementprotocol import Ga4mp


'''
event_type and event_parameters description: https://support.google.com/analytics/answer/9267735
'''

# URL = 'https://www.google-analytics.com/mp/collect'
# MEASUREMENT_ID = 'G-RBPYEH82F1'
# API_SECRET = 'bBQPQwnuTDWJcipSKuO6nw'
# CLIENT_ID = '843904533364-oq0i1g87pvoj9chlf96d1aqfvbun0aia.apps.googleusercontent.com'

if __name__ == '__main__':

    event_type = 'new_custom_event'
    event_parameters = {'cd1': 'a parameter', 'cd2': 'another parameter'}
    ga = Ga4mp(measurement_id = 'G-RBPYEH82F1', api_secret = 'bBQPQwnuTDWJcipSKuO6nw', client_id='843904533364-oq0i1g87pvoj9chlf96d1aqfvbun0aia.apps.googleusercontent.com')

    for _ in range(23):
        ga.add_event(event_type, event_parameters)

    ga.send_hit()














