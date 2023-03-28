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
    '2020.pycon.kr',
]

# https://stackoverflow.com/questions/54784981/django-allauth-google-oauth-redirect-uri-mismatch-error
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

# Append ELB healthcheck hostname(internal ip address)
# https://stackoverflow.com/questions/55718292/getting-400s-from-aws-elb-hostcheck-to-work-with-django-allowed-hosts-in-aws-ec
if 'ECS_CONTAINER_METADATA_URI' in os.environ:
    ELB_HEALTHCHECK_HOSTNAMES = [ip for network in
                                 requests.get(os.environ['ECS_CONTAINER_METADATA_URI']).json()[
                                     'Networks']
                                 for ip in network['IPv4Addresses']]
    print(f'Append ELB healthcheck hostname: {ELB_HEALTHCHECK_HOSTNAMES}')
    ALLOWED_HOSTS += ELB_HEALTHCHECK_HOSTNAMES


aws_env_keys = ['AWS_ACCESS_KEY_ID',
                'AWS_SECRET_ACCESS_KEY', 'AWS_STORAGE_BUCKET_NAME']

for key in aws_env_keys:
    if not os.getenv(key):
        print(f'You should set {key}')
        exit(1)
    else:
        print('{}: {}'.format(key, os.getenv(key)))

INSTALLED_APPS += (
    'collectfast',
)

AWS_DEFAULT_ACL = 'public-read'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
COLLECTFAST_STRATEGY = "collectfast.strategies.boto3.Boto3Strategy"
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = 'ap-northeast-2'
AWS_S3_SIGNATURE_VERSION = 's3v4'

# Django-sass
STATICFILES_STORAGE = 'sass_processor.storage.SassS3Boto3Storage'

# Django-compressor
COMPRESS_OFFLINE = True
LIBSASS_OUTPUT_STYLE = 'compressed'
COMPRESS_URL = 'https://{}.s3.amazonaws.com/'.format(os.getenv('AWS_STORAGE_BUCKET_NAME'))
STATIC_URL = COMPRESS_URL

# https://stackoverflow.com/questions/30801136/django-compressor-is-not-working-on-hosted-static-files-on-amazon-s3
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_STORAGE = STATICFILES_STORAGE

# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
