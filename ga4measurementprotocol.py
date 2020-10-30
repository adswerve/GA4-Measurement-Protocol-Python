# imports
import requests
import sys
import json
import retrying

class Ga4mp(object):

    def __init__(self, measurement_id, api_secret, client_id):
        self.measurement_id = measurement_id
        self.api_secret = api_secret
        self.client_id = client_id
        self.base_url = 'https://www.google-analytics.com/mp/collect'
        self.params_dict = {'earn_virtual_currency': ['virtual_currency_name', 'value'],
                            'join_group': ['group_id'],
                            'login': ['method'],
                            'purchase': ['transaction_id', 'value', 'currency', 'tax', 'shipping', 'items', 'coupon'],
                            'refund': ['transaction_id', 'value', 'currency', 'tax', 'shipping', 'items'],
                            'search': ['search_term'],
                            'select_content': ['content_type', 'item_id'],
                            'share': ['content_type', 'item_id'],
                            'sign_up': ['method'],
                            'spend_virtual_currency': ['item_name', 'virtual_currency_name', 'value'],
                            'tutorial_begin': [],
                            'tutorial_complete': []}


    '''
    event_type and event_parameters description: https://support.google.com/analytics/answer/9267735
    '''

    # URL = 'https://www.google-analytics.com/mp/collect'
    # MEASUREMENT_ID = 'G-RBPYEH82F1'
    # API_SECRET = 'bBQPQwnuTDWJcipSKuO6nw'
    # CLIENT_ID = '843904533364-oq0i1g87pvoj9chlf96d1aqfvbun0aia.apps.googleusercontent.com'

    def send_hit(self, event_type, event_parameters):

        # Check for any missing or invalid parameters
        parameter_keys = event_parameters.keys()
        for x in self.params_dict[event_type]:
            if x not in parameter_keys:
                raise Exception("Event parameters do not match event type.\nFor a breakdown of currently supported event types and their parameters go here: https://support.google.com/analytics/answer/9267735")

        url = f'{self.base_url}?measurement_id={self.measurement_id}&api_secret={self.api_secret}'
        request = {'client_id': self.client_id,
                   'events': [{'name': event_type,
                               'params': event_parameters
                               }]
                   }
        body = json.dumps(request)

        # Send http post request
        r = requests.post(url=url, data=body)
        s = r.status_code
        print(f'Status code: {s}')





