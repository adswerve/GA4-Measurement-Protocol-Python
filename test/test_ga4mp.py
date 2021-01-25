import requests
import json
import copy
import unittest
import pytest

from ga4mp import Ga4mp
from ga4mp.utils import params_dict
from main import MEASUREMENT_ID, API_SECRET, CLIENT_ID
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Ga4mpTestMethods(unittest.TestCase):

    def test_check_params_1_events_correct(self):

        events_correct = [{'name': 'level_end',
          'params': {'level_name': 'First',
                     'success': 'True'}
          },
         {'name': 'level_up',
          'params': {'character': 'John Madden',
                     'level': 'First'}
          }]

        Ga4mp._check_params(self, events_correct)

        assert True

    def test_check_params_2_events_not_a_list(self):

        events_not_a_list = ({'name': 'level_end',
                   'params': {'level_name': 'First',
                              'success': 'True'}
                   },
                  {'name': 'level_up',
                   'params': {'character': 'John Madden',
                              'level': 'First'}
                   })
        with pytest.raises(AssertionError, match="events should be a list"):
            Ga4mp._check_params(self, events_not_a_list)

    def test_check_params_3_event_not_a_dict(self):

        events_event_not_a_dict = [{'name': 'level_end',
                     'params': {'level_name': 'First',
                                'success': 'True'}
                     },
                    ['name', 'level_up', 'params', {'character': 'John Madden',
                                'level': 'First'}
                     ]]

        with pytest.raises(AssertionError, match="each event should be a dictionary"):
            Ga4mp._check_params(self, events_event_not_a_dict)

    def test_check_params_4_events_incorrect_key(self):

        events_incorrect_key = [{'incorrect_key': 'level_end',
                     'params': {'level_name': 'First',
                                'success': 'True'}
                     },
                    {'name': 'level_up',
                     'params': {'character': 'John Madden',
                                'level': 'First'}
                     }]

        with pytest.raises(AssertionError, match="each event should have a name key"):
            Ga4mp._check_params(self, events_incorrect_key)


    def test_check_params_5_warning(self):

        events_should_get_warning = [{'name': 'level_end',
                                      'params' : {'level_name': 'First',
                                                  'incorrect_key': 'True'}
                                     }]


        Ga4mp._check_params(self, events_should_get_warning)

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