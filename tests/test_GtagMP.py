import unittest
import json
import logging
import os, sys

sys.path.append(
    os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
)

from ga4mp.ga4mp import GtagMP

# Get credentials
try:
    credentials = json.load(open("./credentials/credentials.json"))
    MEASUREMENT_ID = credentials["MEASUREMENT_ID"]
    API_SECRET = credentials["API_SECRET"]
except:
    raise RuntimeError("Failed to get Measurement ID and/or API Secret Key from './credentials/credentials.json'")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class TestGtagMPClient(unittest.TestCase):
    def test_check_params_1_events_correct(self):
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

        GtagMP._check_params(self, events_correct)

        assert True

if __name__ == "__main__":
    unittest.main()