import unittest
import json
import logging
import os, sys
import pytest
from testfixtures import log_capture

sys.path.append(
    os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
)

from ga4mp.ga4mp import GtagMP

# Get credentials
try:
    credentials = json.load(open("./credentials/credentials.json"))
    MEASUREMENT_ID = credentials["MEASUREMENT_ID"]
    API_SECRET = credentials["API_SECRET"]
    CLIENT_ID = credentials["CLIENT_ID"]
except:
    raise RuntimeError("Failed to get Measurement ID and/or API Secret Key from './credentials/credentials.json'")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class TestGtagMPClientInternalParamFunctions(unittest.TestCase):
    def setUp(self):
        self.gtag = GtagMP(api_secret=API_SECRET, measurement_id=MEASUREMENT_ID, client_id=CLIENT_ID)

    def test_check_params_events_correct(self):
        events_correct = [
            {
                'name': 'level_end',
                'params': {
                    'level_name': 'First',
                    'success': 'True'
                }
            },
            {
                'name': 'level_up',
                'params': {
                    'character': 'The Dude',
                    'level': 'Second'
                }
            }
        ]

        self.gtag._check_params(events_correct)

        assert True
    
    def test_check_params_events_not_in_a_list(self):
        events_not_a_list = (
            {
                'name': 'level_end',
                'params': {
                    'level_name': 'First',
                    'success': 'True'
                }
            },
            {
                'name': 'level_up',
                'params': {
                    'character': 'The Dude',
                    'level': 'Second'
                }
            }
        )
        with pytest.raises(AssertionError, match="events should be a list"):
            self.gtag._check_params(events_not_a_list)
    
    def test_check_params_event_not_a_dict(self):
        event_not_a_dict = [
            [
                'name',
                'level_up',
                'params',
                {
                    'character': 'The Dude',
                    'level': 'Second'
                }
            ]
        ]

        with pytest.raises(AssertionError, match="each event should be an instance of a dictionary"):
            self.gtag._check_params(event_not_a_dict)

    def test_check_params_events_incorrect_key(self):
        event_incorrect_key = [
            {
                'incorrect_key': 'level_up',
                'params': {
                    'character': 'The Dude',
                    'level': 'Second'
                }
            }
        ]

        with pytest.raises(AssertionError, match='each event should have a "name" key'):
            self.gtag._check_params(event_incorrect_key)

    @log_capture()
    def test_check_params_warning(self, capture):
        event_should_get_warning = [
            {
                'name': 'level_end',
                'params': {
                    'level_name': 'First',
                    'incorrect_key': 'True'
                }
            }
        ]

        self.gtag._check_params(event_should_get_warning)

        expected_log = ('ga4mp.ga4mp', 'WARNING', "WARNING: Event parameters do not match event type.\nFor level_end event type, the correct parameter(s) are ['level_name', 'success'].\nThe parameter 'success' triggered this warning.\nFor a breakdown of currently supported event types and their parameters go here: https://support.google.com/analytics/answer/9267735\n")

        capture.check(expected_log)

if __name__ == "__main__":
    unittest.main()