
import requests
import json

from ga4mp import Ga4mp
from main import MEASUREMENT_ID, API_SECRET, CLIENT_ID

class Ga4mpTest(Ga4mp):

    def _http_post(self, batched_event_list, validation_hit=False):
        """
        Method to send http POST request to google-analytics.

        Parameters
        ----------
        batched_event_list : List[List[Dict]]
            List of List of events. Places initial event payload into a list to send http POST in batches.
        validation_hit : bool, optional
            Boolean to depict if events should be tested against the Measurement Protocol Validation Server, by default False
        """

        # this is the change from the parent class. We need this var to be global for validation/testing
        global status_code

        # set domain
        domain = self._base_domain
        if validation_hit == True:
            domain = self._validation_domain

        # loop through events in batches of 25
        batch_number = 1
        for batch in batched_event_list:
            url = f'{domain}?measurement_id={self.measurement_id}&api_secret={self.api_secret}'

            # this will return code 404 and will fail the test_http_status_code()
            # url = f'{domain}testAddURLPartToBreakProgram?measurement_id={self.measurement_id}&api_secret={self.api_secret}'

            request = {'client_id': self.client_id,
                       'events': batch}
            body = json.dumps(request)

            # Send http post request
            result = requests.post(url=url, data=body)
            status_code = result.status_code
            print(f'Batch Number: {batch_number}\nStatus code: {status_code}')
            batch_number += 1

def test_http_status_code():

    # Create an instance of GA4 object
    ga = Ga4mpTest(measurement_id = MEASUREMENT_ID, api_secret = API_SECRET, client_id=CLIENT_ID)

    # Specify event type and parameters
    event_type = 'new_custom_event_meow'
    event_parameters = {'paramater_key_1': 'parameter_1', 'paramater_key_2': 'parameter_2'}
    event = {'name': event_type, 'params': event_parameters }
    events = [event]

    # Send a custom event to GA4 immediately
    ga.send(events)

    # Postponed send of a custom event to GA4
    # ga.send(events, postpone=True)
    # ga.postponed_send()

    acceptable_http_status_codes = [200, 201, 204]

    assert status_code in acceptable_http_status_codes
