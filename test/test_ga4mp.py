import requests
import json
import copy
import unittest

from ga4mp import Ga4mp
from ga4mp.utils import params_dict
from main import MEASUREMENT_ID, API_SECRET, CLIENT_ID
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Ga4mpTestMethods(unittest.TestCase):
    def test_http_status_code(self):

        # Create an instance of GA4 object
        ga = Ga4mp(
            measurement_id=MEASUREMENT_ID, api_secret=API_SECRET, client_id=CLIENT_ID
        )

        # Specify event type and parameters
        event_type = "new_custom_event"
        event_parameters = {
            "paramater_key_1": "parameter_1",
            "paramater_key_2": "parameter_2",
        }
        event = {"name": event_type, "params": event_parameters}
        events = [event]
        batched_event_list = [events[event:event + 25] for event in range(0, len(events), 25)]
        status_code = ga._http_post(batched_event_list)

        # Send a custom event to GA4 immediately
        # ga.send(events)

        acceptable_http_status_codes = [200, 201, 204]

        assert status_code in acceptable_http_status_codes

    def test_append_event_to_params_dict(self):

        params_dict_test = copy.deepcopy(params_dict)
        params_dict_test.update(
            {"new_name": ["new_param_1", "new_param_2", "new_param_3"]}
        )

        assert params_dict_test["new_name"]


if __name__ == "__main__":
    unittest.main()