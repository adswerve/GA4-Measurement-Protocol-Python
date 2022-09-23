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
    CLIENT_ID = credentials["CLIENT_ID"]
except:
    raise RuntimeError("Failed to get Measurement ID and/or API Secret Key from './credentials/credentials.json'")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class TestGtagMPClientInternalUtilityFunctions(unittest.TestCase):
    def setUp(self):
        self.gtag = GtagMP(api_secret=API_SECRET, measurement_id=MEASUREMENT_ID, client_id=CLIENT_ID)

    def test_create_client_id(self):
        test_cid = self.gtag.random_client_id()

        self.assertRegex(test_cid,r"\d{10}\.\d{10}")

if __name__ == "__main__":
    unittest.main()