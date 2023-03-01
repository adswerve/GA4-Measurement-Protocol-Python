import unittest
import json
import logging
import os, sys
import datetime

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

class TestGtagMPClientValidation(unittest.TestCase):
    def setUp(self):
        self.gtag = GtagMP(api_secret=API_SECRET, measurement_id=MEASUREMENT_ID, client_id=CLIENT_ID)

        # Build test events list
        self.event_list = [
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

        self.malformed_event_list = [
            {
                'name': '',
                'params': {
                    'level_name': 'First',
                    'success': 'True'
                }
            },
            {
                'name': 'level_up',
                'params': {
                    'character': {},
                    'level': 'Second'
                }
            }
        ]

        self.acceptable_http_status_codes = [200, 201, 204]

    def test_http_status_code(self):
        status_code = self.gtag._http_post(self.event_list, validation_hit=True)

        assert status_code in self.acceptable_http_status_codes

    def test_http_status_code_with_datetime_arg(self):
        dt = datetime.datetime.now()

        status_code = self.gtag._http_post(self.event_list, validation_hit=True, date=dt)

        assert status_code in self.acceptable_http_status_codes
    
    def test_malformed_events_log_error_messages(self):
        with self.assertLogs() as captured:
            status_code = self.gtag._http_post(self.malformed_event_list, validation_hit=True)
        self.assertEqual(len(captured.records), 9)
        self.assertEqual(captured.records[3].getMessage(), "| Validation messages:")
        self.assertEqual(captured.records[7].getMessage(), "| Validation messages:")


        assert status_code in self.acceptable_http_status_codes

    def test_http_status_code_with_datetime_delta(self):
        dt = datetime.datetime.now() - datetime.timedelta(hours=1)

        status_code = self.gtag._http_post(self.event_list, validation_hit=True, date=dt)

        assert status_code in self.acceptable_http_status_codes

if __name__ == "__main__":
    unittest.main()