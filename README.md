# GA4 Measurement Protocol Support for Python

This library provides an interface for sending data to Google Analytics, supporting the GA4 Measurement Protocol.

**NOTE**: This project is in *beta* and will be continually updated to cover relevant features of the GA4 Measurement Protocol. Please feel free to file issues for feature requests.

[Meet the next generation of Google Analytics: Learn about the new Google Analytics and how to get started](https://support.google.com/analytics/answer/10089681)

## Contact

Email: `analytics-help@adswerve.com`

## Installation

The easiest way to install GA4 Measurement Protocol Support for Python is directly from PyPi using `pip` by running the following command:

`pip install ga4mp`


## Usage
> **NOTE**: Recent changes have added new platform specific subclasses. In order to take advantage of new functionality, you will need to update the class name of the GA4 object(s) being created in your code.

This library supports both gtag and Firebase data collection models. When creating your tracking object, use either `GtagMP` or `FirebaseMP`, depending on your needs.

The required credentials for sending events to GA4 using **gtag** comprise the following:

| Credential     | Description                                                                                                                                                                                               |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| api_secret     | Generated throught the Google Analytics UI. To create a new secret, navigate in the Google Analytics UI to: **Admin** > **Data Streams** > **choose your stream** > **Measurement Protocol API secrets** > **Create** |
| measurement_id | The identifier for a Data Stream. Found in the Google Analytics UI under:  **Admin** > **Data Streams** > **choose your stream** > **Measurement ID**                                                     |
| client_id      | A unique identifier for a client, representing a specific browser/device.                                                                                                                                 |

The required credentials for sending events to **Firebase** comprise the following:

| Credential      | Description                                                                                                                                                                                               |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| api_secret      | Generated throught the Google Analytics UI. To create a new secret, navigate in the Google Analytics UI to: **Admin** > **Data Streams** > **choose your stream** > **Measurement Protocol API secrets** > **Create** |
| firebase_app_id | The identifier for a Firebase app. Found in the Firebase console under: **Project Settings** > **General** > **Your Apps** > **App ID**.                                                                  |
| app_instance_id | A unique identifier for a Firebase app instance. See [Required parameters > 2. JSON body](https://developers.google.com/analytics/devguides/collection/protocol/ga4/sending-events?client_type=firebase#required_parameters) for details. |

Create your *credentials.json* file and put in your "./credentials" subdirectory.

``` json
{"API_SECRET": "<YOUR_API_SECRET>",
 "MEASUREMENT_ID": "<YOUR_MEASUREMENT_ID>",
 "CLIENT_ID": "<YOUR_CLIENT_ID>",
 "FIREBASE_APP_ID": "<YOUR_FIREBASE_APP_ID>",
 "APP_INSTANCE_ID": "<YOUR_APP_INSTANCE_ID>"}
```

## Memory Storage
In order to solve questions around persistence, this library includes two options for storage:
* `DictStore`, a built-in dictionary class that will persist for the life of the tracking object
* `FileStore`, a built-in dictionary class that will read from and save to a JSON file in a specified location

Use of one of these two is required for session parameters (e.g., `session_id`) and user properties, so initialization of the tracking object will also initialize a default `DictStore`. 

If you wish to load in your own dictionary, load a JSON file, or opt to use `FileStore` instead, you may do so immediately after initializing the tracking object. For any of these, use the following command from your tracking object:
`create_store(use_file, store, session_id, data_location)`
* `use_file`: This argument defaults to false, so you may omit it if using `DictStore`.
* `store`: If using `DictStore`, you may supply your own dictionary, which will automatically be used in the `load(data)` command below. Omit this parameter if using `FileStore` or starting from scratch.
* `session_id`: This session parameter is required for certain types of reporting in GA4/Firebase. If you wish to manually set a session_id, use this parameter. Omitting this will default to any session_id included in a loaded `DictStore` or `FileStore`; however, if one is not available, it will then automatically construct a session_id.
* `data_location`: If using `FileStore`, you must specify where the JSON file exists (or should be created if not yet existing). See `load(data_location)` command below for more details.

### Built-In Memory Storage Commands (DictStore Specific)
* `load(data)`: Overwrite the current contents of the dictionary. `data` must be an instance of a dictionary.
* `save()`: Returns the current contents of the dictionary so that you can save them outside of the tracking object.

### Built-In Memory Storage Commands (FileStore Specific)
* `load(data_location)`: Overwrite the current contents of the tracking object's dictionary with the contents of a JSON file at the given `data_location`. If a JSON file does not exist, it will try to create a new JSON file containing an empty object (i.e., `{}`). When using make sure `data_location` includes the path to the file as well as its name and extension (e.g., `./temp/store.json`).
* `save(data_location)`: Try to overwrite the JSON file at the given `data_location` with the current contents of the tracking object's dictionary. The `data_location` argument is optional: if not supplied, this will try to save to the same location used in the `load(data_location)` command.

### Built-In Memory Storage Commands (Both Classes)
> **NOTE**: The memory storage classes operate on 3 different types of data: **user properties**, which are sent to GA/Firebase with all events, **session parameters**, which should temporarily store information relevant to a single session (e.g., a session ID or the last time an event was sent), and **other**, for anything else you might want to save that wouldn't be sent to GA/Firebase.

Use one of the following to set a new `value` with key `name` as a user property, session parameter, or other type of stored data:
* `set_user_property(name, value)`
* `set_session_parameter(name, value)`
* `set_other_parameter(name, value)`

Use one of the following to get the value of key `name` for a user property, session parameter, or other type of stored data:
* `get_user_property(name)`
* `get_session_parameter(name)`
* `get_other_parameter(name)`

Use one of the following to get all keys and values stored as a user property, session parameter, or other type of stored data:
* `get_all_user_properties()`
* `get_all_session_parameters()`
* `get_all_other_parameters()`

Use one of the following to clear all keys and values stored as a user property, session parameter, or other type of stored data:
* `clear_user_properties()`
* `clear_session_parameters()`
* `clear_other_parameters()`

## Events and Ecommerce Items
While you may construct your own events and ecommerce items as dictionaries, the built-in Event and Item classes should eliminate guesswork about how to properly structure them.

### Creating an Event
To create an event, begin by using the following command from your tracking object:
`create_new_event(name)`
* `name`: Corresponds to the Event Name that you would want to see in your GA4/Firebase reporting. Per Google's requirements, Event Names must be 40 characters or fewer, may only contain alpha-numeric characters and underscores, and must start with an alphabetic character.

The function will return an Event object with its own functions (see below). Once the Event is complete, you will be able to pass it to your tracking object's `send()` function within a list of 1 or more events.

### Creating an Item
While building an ecommerce event, create a new item by using the following command from your Event object: `create_new_item(item_id, item_name)`
* `item_id`: The product SKU for the specific item.
* `item_name`: The name for the specific item.

At least one of `item_id` or `item_name` must be included; however, it is recommended to use both, if applicable.

The function will return an Item object with its own functions (see below). Once the Item is complete, you will be able to pass it to the associated Event object's `add_item_to_event()` function.

## Example Code
The following represents a simple example of a custom event sent to GA4:
``` python
from ga4mp import gtagMP, firebaseMP

# Create an instance of GA4 object using gtag...
ga = GtagMP(api_secret = <API_SECRET>, measurement_id = <MEASUREMENT_ID>, client_id=<CLIENT_ID>)

# ...or create an object using Firebase.
ga = FirebaseMP(api_secret = <API_SECRET>, firebase_app_id=<FIREBASE_APP_ID>, app_instance_id=<CLIENT_ID>)

# Specify event type and parameters
event_type = 'new_custom_event'
event_parameters = {'parameter_key_1': 'parameter_1', 'parameter_key_2': 'parameter_2'}
event = {'name': event_type, 'params': event_parameters }
events = [event]

"""
Events need to be passed as a list of dictionaries, fitting the format:
[{'name': 'level_end',
  'params' : {'level_name': 'First',
              'success': 'True'}
 },
 {'name': 'level_up',
  'params': {'character': 'John Madden',
             'level': 'First'}
 }]
"""

# Set persistent user properties
# Includes user_id, non_personalized_ads, and all else set as custom user_properties
ga.set_user_property('user_id', 'Thales2000')
ga.set_user_property('customer_tier','enterprise')

# Remove a user property
ga.delete_user_property('user_id')

# Send a custom event to GA4 immediately
ga.send(events)

# Postponed send of a custom event to GA4
ga.send(events, postpone=True)
ga.postponed_send()

# Generate and set a new, random Client ID (gtagMP objects only)
ga.client_id = ga.random_client_id()
```

## Google Developer Documentation
Some relevant documentation from Google may be found below...

### How to construct Events
For more information on constructing events, please review the [GA4 Measurement Protocol reference](https://developers.google.com/analytics/devguides/collection/protocol/ga4/reference).

### User properties
For more information on what user properties are in GA4 and what you can do with them, [please review here](https://developers.google.com/analytics/devguides/collection/protocol/ga4/user-properties?client_type=gtag)

## License
GA4 Measurement Protocol Support for Python is licensed under the [BSD License](./LICENSE).
