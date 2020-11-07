# Ga4-Measurement-Protocol-Python

## 1. Purpose

Collects/sends data to Google Analytics 4 (GA4).


## 2. Background
[Meet the next generation of Google Analytics: Learn about the new Google Analytics and how to get started](https://support.google.com/analytics/answer/10089681)


## 3. Project set up

### 3.1 Create a Google Analytics 4 acccount or upgrade from Universal Analytics.


[Upgrade to a Google Analytics 4 property
Set up a Google Analytics 4 property (formerly known as an App + Web property) alongside your existing Universal Analytics property.](https://support.google.com/analytics/answer/9744165?hl=en)


### 3.2 Obtain credentials


#### 3.2.1 MEASUREMENT_ID

- GA
- Admin
- Data Streams
- choose your stream
- MEASUREMENT ID



#### 3.2.2 API_SECRET

- GA
- Admin
- Data Streams
- choose your stream
- Measurement Protocol API Secrets 
- Review Terms and Acknowledge
- Create
- Enter Nickname
- Record *Secret value*

#### 3.2.3 CLIENT_ID

[Get your Google API client ID](https://developers.google.com/identity/one-tap/web/guides/get-google-api-clientid)


### 3.3 Install requirements

```
pip install requirements
```


### 3.4 Run the program

Run main.py

