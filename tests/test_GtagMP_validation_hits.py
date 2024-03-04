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

    def test_http_status_code(self):
        dictionary = self.gtag._http_post(self.event_list, validation_hit=True)

        self.assertIsInstance(dictionary, dict) 

    def test_http_status_code_with_datetime_arg(self):
        dt = datetime.datetime.now()

        dictionary = self.gtag._http_post(self.event_list, validation_hit=True, date=dt)

        self.assertIsInstance(dictionary, dict) 
    
    def test_malformed_events_log_error_messages(self):
        with self.assertLogs() as captured:
            dictionary = self.gtag._http_post(self.malformed_event_list, validation_hit=True)
        self.assertEqual(len(captured.records), 5)
        self.assertEqual(captured.records[3].getMessage(), "| Validation messages:")


        self.assertIsInstance(dictionary, dict) 

    def test_http_status_code_with_datetime_delta(self):
        dt = datetime.datetime.now() - datetime.timedelta(hours=1)

        dictionary = self.gtag._http_post(self.event_list, validation_hit=True, date=dt)

        self.assertIsInstance(dictionary, dict) 

if __name__ == "__main__":
    unittest.main()