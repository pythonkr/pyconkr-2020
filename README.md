# PyCon Korea Homepage

![test-deploy](https://github.com/pythonkr/pyconkr/workflows/test-deploy/badge.svg)

## Requiremensts

- Python 3.7.6

## Getting started

```bash
$ git clone git@github.com:pythonkr/pyconkr.git
$ cd pyconkr
$ pip install -r requirements.txt
$ python manage.py compilemessages
$ python manage.py makemigrations  # flatpages
$ python manage.py migrate
$ python manage.py loaddata ./pyconkr/fixtures/flatpages.json
$ bower install
$ python manage.py runserver
```

For Install bower
```
$ sudo npm install -g bower
```