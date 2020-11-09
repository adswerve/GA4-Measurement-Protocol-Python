# import time
# import requests
# import sys
# import json
# import retrying
from ga4measurementprotocol import Ga4mp

#TODO: remove not used imports?

'''
event_type and event_parameters description: https://support.google.com/analytics/answer/9267735
'''
#TODO: later we'll remove developer testing credentials
# Nate's credentials
# MEASUREMENT_ID = 'G-RBPYEH82F1'
# API_SECRET = 'bBQPQwnuTDWJcipSKuO6nw'
# CLIENT_ID = '843904533364-oq0i1g87pvoj9chlf96d1aqfvbun0aia.apps.googleusercontent.com'

# Ruslan's credentials
MEASUREMENT_ID = 'G-F7PBQ0K03Q'
API_SECRET = 'b7o6YyW7Qu6LO8dfOu-NZA'
CLIENT_ID = '522429634784-9ir6cinsb7sk2c0t9i9dd8evreg7co1f.apps.googleusercontent.com'

if __name__ == '__main__':

    # runs
    event_type = 'new_custom_event'
    event_parameters = {'cd1': 'a parameter', 'cd2': 'another parameter'}

    # gives a warning
    # event_type = 'ad_click'
    # event_parameters ={'content_type': 'test_add_event_id'}

    ga = Ga4mp(measurement_id = MEASUREMENT_ID, api_secret = API_SECRET, client_id=CLIENT_ID)

    for _ in range(3):
        # ga.add_event(event_type + str(i+100), event_parameters)
        ga.add_event(event_type, event_parameters)
        # time.sleep(0.01)

    ga.send_hit()













