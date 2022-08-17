import unittest
import logging
from ga4mp import Ga4mp
import datetime
from main import MEASUREMENT_ID, API_SECRET, CLIENT_ID

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Ga4mpTestUserProperties(unittest.TestCase):
    def test_add_user_properties(self):

        dt = datetime.datetime.now()

        ga = Ga4mp(
            measurement_id=MEASUREMENT_ID, api_secret=API_SECRET, client_id=CLIENT_ID
        )

        ga.set_user_property('user_id','BabyYoda2000')
        ga.set_user_property('non_personalized_ads', True)
        ga.set_user_property('enterprise', False)


        event_type = "test_add_user_properties"
        event_parameters = {
            "paramater_key_1": "testing - " + str(dt)
        }
        event = {"name": event_type, "params": event_parameters}
        events = [event]
        batched_event_list = [
            events[event : event + 25] for event in range(0, len(events), 25)
        ]
        status_code = ga._http_post(batched_event_list, date=dt)

        acceptable_http_status_codes = [200, 201, 204]

        assert status_code in acceptable_http_status_codes



    def test_delete_user_properties(self):

        dt = datetime.datetime.now()

        ga = Ga4mp(
            measurement_id=MEASUREMENT_ID, api_secret=API_SECRET, client_id=CLIENT_ID
        )

        ga.set_user_property('user_id','BabyYoda2000')
        ga.set_user_property('non_personalized_ads', True)
        ga.set_user_property('enterprise', False)

        ga.delete_user_property('user_id')
        ga.delete_user_property('non_personalized_ads')
        ga.delete_user_property('enterprise')
        
        event_type = "delete_add_user_properties"
        event_parameters = {
            "paramater_key_1": "testing - " + str(dt)
        }
        event = {"name": event_type, "params": event_parameters}
        events = [event]
        batched_event_list = [
            events[event : event + 25] for event in range(0, len(events), 25)
        ]
        status_code = ga._http_post(batched_event_list, date=dt)

        acceptable_http_status_codes = [200, 201, 204]

        assert status_code in acceptable_http_status_codes


if __name__ == "__main__":
    unittest.main()
