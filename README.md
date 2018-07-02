sirena-quota
============

It's the best way to control tickets quota in Sirena.
Notice, these scripts works with Sirena Web Services (SWC), not with Sirena XML Gate.

Behold, the power of:
```
$ python checker.py
OTA.UT               - ok
$ python informer.py
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
