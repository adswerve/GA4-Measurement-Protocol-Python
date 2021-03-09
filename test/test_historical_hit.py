import unittest
import logging
from ga4mp import Ga4mp
import datetime
from main import MEASUREMENT_ID, API_SECRET, CLIENT_ID

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Ga4mpTestHistoricalHit(unittest.TestCase):
    def test_datetime_arg(self):
        dt = datetime.datetime.now()

        ga = Ga4mp(
            measurement_id=MEASUREMENT_ID, api_secret=API_SECRET, client_id=CLIENT_ID
        )

        event_type = "test_datetime_now"
        event_parameters = {
            "paramater_key_1": "parameter_1",
        }
        event = {"name": event_type, "params": event_parameters}
        events = [event]
        batched_event_list = [
            events[event : event + 25] for event in range(0, len(events), 25)
        ]
        status_code = ga._http_post(batched_event_list, date=dt)

        acceptable_http_status_codes = [200, 201, 204]

        assert status_code in acceptable_http_status_codes

    def test_datetime_delta(self):

        dt = datetime.datetime.now() - datetime.timedelta(hours=1)

        ga = Ga4mp(
            measurement_id=MEASUREMENT_ID, api_secret=API_SECRET, client_id=CLIENT_ID
        )
        logger.info("Running 48hr")
        event_type = "test_datetime_48hr"
        event_parameters = {
            "paramater_key_1": "parameter_1",
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
