import requests
import json

from main import MEASUREMENT_ID, API_SECRET, CLIENT_ID
from ga4measurementprotocol import Ga4mp


class Ga4mpTest(Ga4mp):

    def send_hit(self, validation_hit=False):

        global s

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
            r = requests.post(url=url, data=body)
            s = r.status_code
            print(f'Batch Number: {batch_number}\nStatus code: {s}')
            batch_number += 1

        self.event_list = []


def test_send_hit():
    event_type = 'new_custom_event_TEST_RB'
    event_parameters = {'cd1': 'a parameter', 'cd2': 'another parameter'}
    ga = Ga4mpTest(measurement_id=MEASUREMENT_ID, api_secret=API_SECRET, client_id=CLIENT_ID)

    acceptable_http_status_codes = [200, 201, 204]

    for _ in range(7):
        ga.add_event(event_type, event_parameters)

    ga.send_hit()

    assert s in acceptable_http_status_codes
