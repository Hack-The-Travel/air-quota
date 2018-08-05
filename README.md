air-quota
=========

It's the best way to control tickets and EMDs quota in Amadeus and Sirena.

GDS dependencies:
- Amadeus Web Services (AWS), SOAP Header 4.0.
- Sirena Web Services (SWC), not Sirena XML Gate.

Behold, the power of:
```
$ python check.py
OTA.1H.UT             - ok
OTA.1A.S7             - ok
$ python inform.py
```


## Installation
First, initialize your virtual environment
```
$ virtualenv .ve
$ source .ve/bin/activate
```

Install dependencies
```
$ pip install -r requirements.txt
```

Setup configuration
```
$ cp conf.sample.py conf.py
$ vim conf.py
✨🎩✨
```

Finally, setup sqlite database
```
$ python manage.py setup
```
