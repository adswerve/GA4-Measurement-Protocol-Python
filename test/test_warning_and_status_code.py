import requests
import json
import random

from main import MEASUREMENT_ID, API_SECRET, CLIENT_ID
from ga4measurementprotocol import Ga4mp


class Ga4mpTest(Ga4mp):

    # # when this function is called it will add a new event to the event_list
    # def add_event(self, event_type, event_parameters):
    #
    #     global give_warning, parameter, parameter_keys
    #
    #     # check for any missing or invalid parameters
    #     parameter_keys = event_parameters.keys()
    #     params = self.get_params(event_type) if self.get_params(event_type) is not None else []
    #
    #     for parameter in params:
    #         if parameter not in parameter_keys:
    #             give_warning = True
    #             print(
    #                 f"WARNING: Event parameters do not match event type.\nFor {event_type} event type, the correct parameter(s) are {params}.\nFor a breakdown of currently supported event types and their parameters go here: https://support.google.com/analytics/answer/9267735\n")
    #
    #     new_event = {'name': event_type,
    #                  'params': event_parameters}
    #     self.event_list.append(new_event)

    def send(self, validation_hit=False):

        global status_code

        domain = self.base_domain
        if validation_hit == True:
            domain = self.validation_domain

        batched_event_list = [self.event_list[event:event + 25] for event in range(0, len(self.event_list), 25)]
        batch_number = 1
        for batch in batched_event_list:
            url = f'{domain}?measurement_id={self.measurement_id}&api_secret={self.api_secret}'
            # this will return code 404 and will fail the test_send_hit() test
            # url = f'{domain}testAddURLPartToBreakProgram?measurement_id={self.measurement_id}&api_secret={self.api_secret}'

            request = {'client_id': self.client_id,
                       'events': batch
                       }
            body = json.dumps(request)

            # Send http post request
            result = requests.post(url=url, data=body)
            status_code = result.status_code
            print(f'Batch Number: {batch_number}\nStatus code: {status_code}')
            batch_number += 1

        self.event_list = []


testing_dict = {'custom_event_unit_test_1':{'cd1': 'a parameter', 'cd2': 'another parameter'},
                'custom_event_unit_test_2': {'cd2': 'parameter_1', 'cd4': 'parameter_2'},
                'ad_click' : {'ad_event_id': 'test_value'},
                'ad_exposure' : {'ad_event_id': 'test_value'}, # this will give a warning, as these are incorrect parameters
                'video_start' : {'content_type': 'test_value'}
                }


index = random.randint(0, len(testing_dict) - 1)

number_of_events = random.randint(1,10)

event_type = list(testing_dict.keys())[index]

event_parameters = testing_dict.get(event_type)


def test_add_event():
    ga = Ga4mpTest(measurement_id=MEASUREMENT_ID, api_secret=API_SECRET, client_id=CLIENT_ID)

    ga.add_event(event_type, event_parameters)

    if parameter not in parameter_keys:
        assert give_warning


def test_send_hit():

    ga = Ga4mpTest(measurement_id=MEASUREMENT_ID, api_secret=API_SECRET, client_id=CLIENT_ID)

    acceptable_http_status_codes = [200, 201, 204]

    for i in range(number_of_events):
        # ga.add_event(event_type + str(i+number_of_events), event_parameters) # to give each event a unique name
        ga.add_event(event_type, event_parameters)

    print(f"Sending {number_of_events} hits of {event_type} event with with parameters {event_parameters}")

    ga.send_hit()

    assert status_code in acceptable_http_status_codes
