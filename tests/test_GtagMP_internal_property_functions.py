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

class TestGtagMPClientInternalPropertyFunctions(unittest.TestCase):
    def setUp(self):
        self.gtag = GtagMP(api_secret=API_SECRET, measurement_id=MEASUREMENT_ID, client_id=CLIENT_ID)

    def test_add_user_property(self):
        self.gtag.store.set_user_property("user_id","Grogu")
        
        self.assertEqual(self.gtag.store["user_properties"]["user_id"], "Grogu")

    def test_add_multiple_user_properties(self):
        self.gtag.store.set_user_property("user_id","Grogu")
        self.gtag.store.set_user_property("region","Outer Rim")

        self.assertEqual(len(self.gtag.store), 2)
        
    def test_delete_user_property(self):
        self.gtag.store.set_user_property("user_id","Grogu")
        self.gtag.store.set_user_property("region","Outer Rim")

        self.gtag.store.delete_user_property("user_id")

        self.assertFalse("user_id" in self.gtag.store.keys())

if __name__ == "__main__":
    unittest.main()