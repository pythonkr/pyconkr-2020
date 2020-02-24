from pyconkr.settings import *
import os
import requests

DEBUG = False
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'www.pycon.kr',
    'dev.pycon.kr',
    'pycon.kr',
]

# Append ELB healthcheck hostname(internal ip address)
# https://stackoverflow.com/questions/55718292/getting-400s-from-aws-elb-hostcheck-to-work-with-django-allowed-hosts-in-aws-ec
if 'ECS_CONTAINER_METADATA_URI' in os.environ:
    ELB_HEALTHCHECK_HOSTNAMES = [ip for network in
                                 requests.get(os.environ['ECS_CONTAINER_METADATA_URI']).json()[
                                     'Networks']
                                 for ip in network['IPv4Addresses']]
    print(f'Append ELB healthcheck hostname: {ELB_HEALTHCHECK_HOSTNAMES}')
    ALLOWED_HOSTS += ELB_HEALTHCHECK_HOSTNAMES
