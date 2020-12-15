###############################################################################
# Google Analytics 4 Measurement Protocol for Python
# Copyright (c) 2020, Analytics Pros
#
# This project is free software, distributed under the BSD license.
# Analytics Pros offers consulting and integration services if your firm needs
# assistance in strategy, implementation, or auditing existing work.
###############################################################################

import requests
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


from ga4mp.utils import params_dict


class Ga4mp(object):
    """
    Class that provides an interface for sending data to Google Analytics, supporting the GA4 Measurement Protocol.

    Parameters
    ----------
    measurement_id : string
        The identifier for a Data Stream. Found in the Google Analytics UI under: Admin > Data Streams > choose your stream > Measurement ID
    api_secret : string
        Generated throught the Google Analytics UI. To create a new secret, navigate in the Google Analytics UI to: Admin > Data Streams >
        choose your stream > Measurement Protocol > Create
    client_id : string
        Getting your Google API client ID: https://developers.google.com/identity/one-tap/web/guides/get-google-api-clientid


    See Also
    --------

    * Measurement Protocol (Google Analytics 4): https://developers.google.com/analytics/devguides/collection/protocol/ga4
    
    Examples
    --------

    >>> ga = Ga4mp(measurement_id = "MEASUREMENT_ID", api_secret = "API_SECRET", client_id="CLIENT_ID")
    >>> event_type = 'new_custom_event'
    >>> event_parameters = {'paramater_key_1': 'parameter_1', 'paramater_key_2': 'parameter_2'}
    >>> event = {'name': event_type, 'params': event_parameters }
    >>> events = [event]

    # Send a custom event to GA4 immediately
    >>> ga.send(events)

    # Postponed send of a custom event to GA4
    >>> ga.send(events, postpone=True)
    >>> ga.postponed_send()
    """

    def __init__(self, measurement_id, api_secret, client_id):
        self.measurement_id = measurement_id
        self.api_secret = api_secret
        self.client_id = client_id
        self._event_list = []
        self._base_domain = 'https://www.google-analytics.com/mp/collect'
        self._validation_domain = 'https://www.google-analytics.com/debug/mp/collect'

    def send(self, events, validation_hit=False, postpone=False):
        """
        Method to send an http post request to google analytics with the specified events.

        Parameters
        ----------
        events : List[Dict]
            A list of dictionaries  of the events to be sent to Google Analytics. The list of dictionaries should adhere
            to the following format:

            [{'name': 'level_end',
            'params' : {'level_name': 'First',
                        'success': 'True'}
            },
            {'name': 'level_up',
            'params': {'character': 'John Madden',
                        'level': 'First'}
            }]

        validation_hit : bool, optional
            Boolean to depict if events should be tested against the Measurement Protocol Validation Server, by default False
        postpone : bool, optional
            Boolean to depict if provided event list should be postponed, by default False
        """

        # check for any missing or invalid parameters among automatically collected and recommended event types
        self._check_params(events)

        if postpone == True:
            # build event list to send later
            for event in events:
                self._event_list.append(event)
        else:
            # batch events into sets of 25 events, the maximum allowed.
            batched_event_list = [events[event:event + 25] for event in range(0, len(events), 25)]
            # send http post request
            self._http_post(batched_event_list, validation_hit=validation_hit)

    def postponed_send(self):
        """
        Method to send the events provided to Ga4mp.send(events,postpone=True) 
        """

        # batch events into sets of 25 events
        batched_event_list = [self._event_list[event:event + 25] for event in range(0, len(self._event_list), 25)]

        self._http_post(batched_event_list)

        # clear event_list for future use
        self._event_list = []

    def append_event_to_params_dict(self, new_name_and_parameters):

        """
        Method to append event name and parameters key-value pair to parameters dictionary.

        Parameters
        ----------
        new_name_and_parameters : Dict
            A dictionary with one key-value pair representing a new type of event to be sent to Google Analytics.
            The dictionary should adhere to the following format:

            {'new_name': ['new_param_1', 'new_param_2', 'new_param_3']}
        """

        params_dict.update(new_name_and_parameters)

    def _http_post(self, batched_event_list, validation_hit=False):
        """
        Method to send http POST request to google-analytics.

        Parameters
        ----------
        batched_event_list : List[List[Dict]]
            List of List of events. Places initial event payload into a list to send http POST in batches.
        validation_hit : bool, optional
            Boolean to depict if events should be tested against the Measurement Protocol Validation Server, by default False
        """

        # set domain
        domain = self._base_domain
        if validation_hit == True:
            domain = self._validation_domain
        logger.info(f"Sending POST to: {domain}")

        # loop through events in batches of 25
        batch_number = 1
        for batch in batched_event_list:
            url = f'{domain}?measurement_id={self.measurement_id}&api_secret={self.api_secret}'
            request = {'client_id': self.client_id,
                       'events': batch}
            body = json.dumps(request)

            # Send http post request
            result = requests.post(url=url, data=body)
            status_code = result.status_code
            logger.info(f'Batch Number: {batch_number}')
            logger.info(f'Status code: {status_code}')
            batch_number += 1

    def _check_params(self, events):

        """
        Method to check whether the event payload parameters provided meets supported parameters.

        Parameters
        ----------
        events : List[Dict]
            A list of dictionaries  of the events to be sent to Google Analytics. The list of dictionaries should adhere
            to the following format:

            [{'name': 'level_end',
            'params' : {'level_name': 'First',
                        'success': 'True'}
            },
            {'name': 'level_up',
            'params': {'character': 'John Madden',
                        'level': 'First'}
            }]
        """

        # check for any missing or invalid parameters
        for e in events:
            event_name = e['name']
            event_params = e['params']
            if (event_name in params_dict.keys()):
                for parameter in params_dict[event_name]:
                    if parameter not in event_params.keys():
                        logger.warning(f"WARNING: Event parameters do not match event type.\nFor {event_name} event type, the correct parameter(s) are {params_dict[event_name]}.\nFor a breakdown of currently supported event types and their parameters go here: https://support.google.com/analytics/answer/9267735\n")
