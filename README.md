sirena-quota
============

It's the best way to control tickets quota in Sirena.


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
