import json

from ga4mp import Ga4mp


'''
event_type and event_parameters description: https://support.google.com/analytics/answer/9267735
'''

try:
    credentials = json.load(open("./credentials/credentials.json"))

except:
    credentials = json.load(open("../credentials/credentials.json"))

MEASUREMENT_ID = credentials['MEASUREMENT_ID']
API_SECRET = credentials['API_SECRET']
CLIENT_ID = credentials['CLIENT_ID']


if __name__ == '__main__':

    event_type = 'stuff'
    event_parameters = {'parameter_1': 'parameter_1_value', 'parameter_2': 'parameter_2_value'}

    event = {'name': event_type, 'params': event_parameters}
    events = [event, event, event, event, event,
              event, event, event, event, event,
              event, event, event, event, event,
              event, event, event, event, event,
              event, event, event, event, event,
              event]

    ga = Ga4mp(measurement_id = MEASUREMENT_ID, api_secret = API_SECRET, client_id=CLIENT_ID)


    ga.send(events)
