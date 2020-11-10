import json

from ga4measurementprotocol import Ga4mp


'''
event_type and event_parameters description: https://support.google.com/analytics/answer/9267735
'''

credentials = json.load(open("./credentials/credentials.json"))

MEASUREMENT_ID = credentials['MEASUREMENT_ID']
API_SECRET = credentials['API_SECRET']
CLIENT_ID = credentials['CLIENT_ID']


if __name__ == '__main__':

    event_type = 'new_custom_event_'
    event_parameters = {'parameter_1': 'parameter_1_value', 'parameter_2': 'parameter_2_value'}

    ga = Ga4mp(measurement_id = MEASUREMENT_ID, api_secret = API_SECRET, client_id=CLIENT_ID)

    for _ in range(3):
        ga.add_event(event_type, event_parameters)

    ga.send_hit()













