# Google Analytics GA4 Measurement Protocol Library

This library provides an interface for sending data to Google Analytics 4 properties using Measurement Protocol.

*NOTE* Google Analytics 4 is in Alpha as of the latest update

## Use

BSD 3-Clause license can be found in ./LICENSE

## Contact

analytics-help@adswerve.com


## Background
[Meet the next generation of Google Analytics: Learn about the new Google Analytics and how to get started](https://support.google.com/analytics/answer/10089681)


## Set up

### 1. Create a Google Analytics 4 acccount or upgrade from Universal Analytics.


[Upgrade to a Google Analytics 4 property
Set up a Google Analytics 4 property (formerly known as an App + Web property) alongside your existing Universal Analytics property.](https://support.google.com/analytics/answer/9744165?hl=en)


### 2 Obtain credentials


#### 2.1 MEASUREMENT_ID

- GA
- Admin
- Data Streams
- choose your stream
- MEASUREMENT ID

#### 2.2 API_SECRET

- GA
- Admin
- Data Streams
- choose your stream
- Measurement Protocol API Secrets 
- Review Terms and Acknowledge
- Create
- Enter Nickname
- Record *Secret value*

#### 2.3 CLIENT_ID

[Get your Google API client ID](https://developers.google.com/identity/one-tap/web/guides/get-google-api-clientid)

### Function call example


Send 10 custom event hits
```
event_type = 'new_custom_event'
event_parameters = {'paramater_key_1': 'parameter_1', 'paramater_key_2': 'parameter_2'}

ga = Ga4mp(measurement_id = MEASUREMENT_ID, api_secret = API_SECRET, client_id=CLIENT_ID)

for _ in range(10):
    ga.add_event(event_type, event_parameters)

ga.send_hit()
```


