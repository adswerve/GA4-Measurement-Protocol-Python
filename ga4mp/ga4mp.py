###############################################################################
# Google Analytics 4 Measurement Protocol for Python
# Copyright (c) 2020, Analytics Pros
#
# This project is free software, distributed under the BSD license.
# Analytics Pros offers consulting and integration services if your firm needs
# assistance in strategy, implementation, or auditing existing work.
###############################################################################

import json
import logging
import urllib.request
from time import time
from ga4mp.utils import params_dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
        self._user_properties = {}
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
                event['_timestamp_micros'] = self._get_timestamp()

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

        for event in self._event_list:
            self._http_post([event], postpone=True)

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

    def _http_post(self, batched_event_list, validation_hit=False, postpone=False):
        """
        Method to send http POST request to google-analytics.

        Parameters
        ----------
        batched_event_list : List[List[Dict]]
            List of List of events. Places initial event payload into a list to send http POST in batches.
        validation_hit : bool, optional
            Boolean to depict if events should be tested against the Measurement Protocol Validation Server, by default False
        validation_hit : bool, optional
            Boolean to determine whether to include past timestamp with hit, by default False
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
            self._add_user_props_to_hit(request)

            #make adjustments for postponed hit
            request['events'] = { 'name' : batch['name'], 'params' : batch['params'] } if(postpone) else batch
            if(postpone):
                #add timestamp to hit
                request['timestamp_micros'] = batch['_timestamp_micros']
            
            req = urllib.request.Request(url)
            req.add_header('Content-Type', 'application/json; charset=utf-8')
            jsondata = json.dumps(request)
            json_data_as_bytes = jsondata.encode('utf-8')   # needs to be bytes
            req.add_header('Content-Length', len(json_data_as_bytes))
            result = urllib.request.urlopen(req, json_data_as_bytes)

            status_code = result.status
            logger.info(f'Batch Number: {batch_number}')
            logger.info(f'Status code: {status_code}')
            batch_number += 1

        return status_code

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

        # check to make sure it's a list of dictionaries with the right keys

        assert type(events) == list, "events should be a list"

        for event in events:

            assert type(event) == dict, "each event should be a dictionary"

            assert "name" in event, 'each event should have a "name" key'

            assert "params" in event, 'each event should have a "params" key'

        # check for any missing or invalid parameters

        for e in events:
            event_name = e['name']
            event_params = e['params']
            if (event_name in params_dict.keys()):
                for parameter in params_dict[event_name]:
                    if parameter not in event_params.keys():
                        logger.warning(f"WARNING: Event parameters do not match event type.\nFor {event_name} event type, the correct parameter(s) are {params_dict[event_name]}.\nFor a breakdown of currently supported event types and their parameters go here: https://support.google.com/analytics/answer/9267735\n")

    def set_user_property(self, property, value):

        """
        Method to set user_id, user_properties, non_personalized_ads

        Parameters
        ----------
        property : string
        value: dependent on property (user_id, user_properties - string, non_personalized_ads - bool)
        """
        self._user_properties.update({ property : value })


    def delete_user_property(self, property):

        """
        Method to remove user_id, user_properties, non_personalized_ads

        Parameters
        ----------
        property : string
        """
        try:
            if property in self._user_properties.keys():
                self._user_properties.pop(property)
        except:
            logger.info(f"Failed to delete user property: {property}")

    def _add_user_props_to_hit(self, hit):

        """
        Method is a helper function to add user properties to outgoing hits.

        Parameters
        ----------
        hit : dict
        """
        for key in self._user_properties:
            try:
                if key in ['user_id', 'non_personalized_ads']:
                    hit.update({ key : self._user_properties[key]})
                else:
                    if 'user_properties' not in hit.keys():
                        hit.update({'user_properties' : {} })
                    hit['user_properties'].update({ key : { "value" : self._user_properties[key]}})
            except:
                logger.info(f"Failed to add user property to outgoing hit: {key}")

    def _get_timestamp(self):
        """
        Method returns UNIX timestamp in microseconds for postponed hits.

        Parameters
        ----------
        None
        """
        return int(time() * 1e6)
