import requests
import sys
import json
import retrying
from ga4measurementprotocol import Ga4mp


'''
event_type and event_parameters description: https://support.google.com/analytics/answer/9267735
'''

URL = 'https://www.google-analytics.com/mp/collect'
MEASUREMENT_ID = 'G-RBPYEH82F1'
API_SECRET = 'bBQPQwnuTDWJcipSKuO6nw'
CLIENT_ID = '843904533364-oq0i1g87pvoj9chlf96d1aqfvbun0aia.apps.googleusercontent.com'

if __name__ == '__main__':

    event_type = 'search'
    event_parameters = {'search_term': 'Yeezys'}
    ga = Ga4mp(measurement_id = 'G-RBPYEH82F1', api_secret = 'bBQPQwnuTDWJcipSKuO6nw', client_id='843904533364-oq0i1g87pvoj9chlf96d1aqfvbun0aia.apps.googleusercontent.com')
    ga.send_hit(event_type, event_parameters)




# def send_hit(event_type, event_parameters):
#
#     # The dictionary below defines the events that are recommended for all properties and their required parameters
#     params_dict = {'earn_virtual_currency': ['virtual_currency_name', 'value'],
#                    'join_group': ['group_id'],
#                    'login': ['method'],
#                    'purchase': ['transaction_id', 'value', 'currency', 'tax', 'shipping', 'items', 'coupon'],
#                    'refund': ['transaction_id', 'value', 'currency', 'tax', 'shipping', 'items'],
#                    'search': ['search_term'],
#                    'select_content': ['content_type', 'item_id'],
#                    'share': ['content_type', 'item_id'],
#                    'sign_up': ['method'],
#                    'spend_virtual_currency': ['item_name', 'virtual_currency_name', 'value'],
#                    'tutorial_begin': [],
#                    'tutorial_complete': []}
#
#     # Check for any missing or invalid parameters
#     missing_parameter = False
#     parameter_keys = event_parameters.keys()
#     for x in params_dict[event_type]:
#         if x not in parameter_keys:
#             missing_parameter = True
#
#     try:
#         if missing_parameter == True:
#             raise Exception("Event parameters do not match event type.")
#     except Exception as e:
#         print(e)
#         return
#
#     url = f'{URL}?measurement_id={MEASUREMENT_ID}&api_secret={API_SECRET}'
#     request = {'client_id': CLIENT_ID,
#                'events': [{'name': event_type,
#                            'params': event_parameters
#                             }]
#               }
#     body = json.dumps(request)
#     r = requests.post(url=url, data=body)
#     s = r.status_code
#     print(s)

