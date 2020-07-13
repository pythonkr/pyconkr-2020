# PyCon Korea Homepage

[![test-deploy](https://github.com/pythonkr/pyconkr/workflows/test-deploy/badge.svg)](https://github.com/pythonkr/pyconkr/actions?query=workflow%3Atest-deploy)

## Contribution

Contribution을 제출할 때는 반드시 다음 [가이드라인](./.github/CONTRIBUTING.md)을 따라주세요.

## Requirements

- Python 3.7.6
- yarn

## Getting started

```bash
$ git clone git@github.com:pythonkr/pyconkr.git
$ cd pyconkr
$ pip install -r requirements.txt
$ sudo npm install -g yarn
$ yarn
$ python manage.py compilemessages
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```
