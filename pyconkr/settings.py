import datetime
import os
import sys

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b6&$e@3d_5xorj*ipg-%=bbsy#a3bryr)^45jnhhik%yjm*sqk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
SITE_ID = 1

INSTALLED_APPS = (
                     # django apps
                     'modeltranslation',
                     'django.contrib.admin',
                     'django.contrib.auth',
                     'django.contrib.contenttypes',
                     'django.contrib.sessions',
                     'django.contrib.messages',
                     'django.contrib.sites',
                     'django.contrib.staticfiles',
                     'django.contrib.flatpages',
                     'django.contrib.humanize',
                 ) + (
                     # third-party apps
                     'django_summernote',
                     'rosetta',
                     'crispy_forms',
                     'sorl.thumbnail',
                     'constance',
                     'constance.backends.database',
                     'django_csv_exports',
                     'mail_templated',
                     'import_export',
                     'sass_processor',
                     # 'compressor',
                 ) + (
                     # local apps
                     'pyconkr',
                     'announcement',
                     'user',
                     'sponsor',
                     'program',
                     'registration',
                     'mailing',
                 ) + (
                     'allauth',
                     'allauth.account',
                     'allauth.socialaccount',
                     'allauth.socialaccount.providers.facebook',
                     'allauth.socialaccount.providers.github',
                     'allauth.socialaccount.providers.twitter',
                     'debug_toolbar',
                 )

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'pyconkr.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "pyconkr/templates"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'pyconkr.context_processors.default',
                'pyconkr.context_processors.sponsors',
                'constance.context_processors.config',
            ],
        },
    },
]

WSGI_APPLICATION = 'pyconkr.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

if os.getenv('POSTGRES_NAME'):
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_NAME'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
    }
# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGES = (
    ('ko', _('Korean')),
    ('en', _('English')),
)
LANGUAGE_CODE = 'ko'
MODELTRANSLATION_FALLBACK_LANGUAGES = {
    'default': ('ko', 'en'),
}

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'pyconkr', 'locale'),
    os.path.join(BASE_DIR, 'user', 'locale'),
)

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

FORCE_SCRIPT_NAME = ''
APPEND_SLASH = True
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, "pyconkr/static"),
# )
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')
STATIC_URL = '/static/'

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    # From 2019 we have decided to support github/facebook login
    'allauth.account.auth_backends.AuthenticationBackend',
)

LOGIN_URL = '/2020/login/'
LOGIN_REDIRECT_URL = '/2020/profile/'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = False
# SOCIALACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_AUTO_SIGNUP = False
SOCIALACCOUNT_ADAPTER = 'user.adapter.SocialAdapter'
SOCIALACCOUNT_FORMS = {
    'signup': 'user.forms.SocialSignupForm'
}

if os.getenv('EMAIL_HOST_USER_NO_REPLY'):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = True
    EMAIL_HOST = os.getenv('EMAIL_HOST_NO_REPLY')
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER_NO_REPLY')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD_NO_REPLY')
    EMAIL_PORT = 587
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

DOMAIN = ''

CRISPY_TEMPLATE_PACK = 'bootstrap3'


def static_url(url):
    return os.path.join(STATIC_URL, url)


SUMMERNOTE_CONFIG = {
    'width': '100%',
    'toolbar': [
        ['insert', ['emoji']],
        ['style', ['style']],
        ['font', ['bold', 'italic', 'underline', 'superscript', 'subscript',
                  'strikethrough', 'clear']],
        ['fontsize', ['fontsize']],
        ['color', ['color']],
        ['para', ['ul', 'ol', 'paragraph']],
        ['height', ['height']],
        ['table', ['table']],
        ['insert', ['link', 'picture', 'video', 'hr']],
        ['view', ['fullscreen', 'codeview']],
        ['help', ['help']],
    ],
    'js': (
        static_url('js/summernote-emoji-config.js'),
        static_url('components/summernote-emoji/tam-emoji/js/config.js'),
        static_url('components/summernote-emoji/tam-emoji/js/tam-emoji.min.js'),
    ),
    'css': (
        static_url('components/summernote-emoji/tam-emoji/css/emoji.css'),
        static_url('css/pyconkr.css'),
    ),
    'styleTags': [
        {'title': 'Blockquote', 'tag': 'blockquote', 'className': 'blockquote', 'value': 'bock', }
    ],
}

# ACCOUNT_UNIQUE_EMAIL = False
SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': [
            'read:user',
            'user:email',
        ]
    },
    # Didn't finish yet
    # https://django-allauth.readthedocs.io/en/latest/providers.html#facebook
    'facebook': {
        'METHOD': 'oauth2',
        # 'SDK_URL': '//connect.facebook.net/{locale}/sdk.js',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
        ],
        'EXCHANGE_TOKEN': True,
        # 'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.12',
    }
}

SPEAKER_IMAGE_MAXIMUM_FILESIZE_IN_MB = 5
SPEAKER_IMAGE_MINIMUM_DIMENSION = (500, 500)

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

KST = datetime.timezone(datetime.timedelta(hours=9))

CONSTANCE_CONFIG = {
    'SLACK_TOKEN': ('', '홈페이지에서 파준위 슬랙으로 알림을 보내기 위한 토큰'),
    'SLACK_CHANNEL': ('#bot-test', '홈페이지에서 파준위 슬랙으로 알림을 보낼 채널'),
    'SLACK_INVITATION_ALARM_CHANNEL': ('#bot-test', 'Slack 가입 요청 알림을 보낼 채널'),
    'CFS_NOTI_CHANNEL': ('#bot-test', 'CFS 등록시, 홈페이지에서 파준위 슬랙으로 알림을 보낼 채널'),
    'TOTAL_TICKET': (1800, '판매할 전체 티켓 수량'),
    'CFP_OPEN': (datetime.datetime(2020, 5, 1), 'CFP 오픈'),
    'CFP_CLOSE': (datetime.datetime(2020, 5, 1, tzinfo=KST), 'CFP 마감기간'),
    'OPEN_REVIEW_START': (datetime.datetime(2020, 6, 1, tzinfo=KST), '오픈 리뷰 시작 시점'),
    'OPEN_REVIEW_FINISH': (datetime.datetime(2020, 6, 1, tzinfo=KST), '오픈 리뷰 마감 시점'),
    'PROGRAM_DETAIL_EDITABLE': (True, '발표 설명 수정 가능 여부'),
    'CFS_OPEN': (datetime.datetime(2020, 5, 1), '후원사 모집 오픈'),
    'CFS_CLOSE': (datetime.datetime(2020, 5, 1), '후원사 모집 종료'),
    'CFP_BRIEF_TEMPLATE': ('', 'CFP 간략한 설명 템플릿'),
    'CFP_DESC_TEMPLATE': ('', 'CFP 자세한 설명 템플릿'),
    'VIRTUAL_BOOTH_EDITABLE': (True, '스폰서 Virtual Booth 수정 가능 여부'),
    'VIRTUAL_BOOTH_EDIT_FINISH': (datetime.datetime(2020, 9, 21, tzinfo=KST), '스폰서 Virtual Booth 수정 마감'),
    'VIRTUAL_BOOTH_OPEN': (datetime.datetime(2020, 9, 21, tzinfo=KST), '스폰서 Virtual Booth 공개'),
    'KEYNOTE_RECOMMEND_OPEN': (datetime.datetime(2020, 5, 1, tzinfo=KST), '키노트 연사 추천 오픈'),
    'KEYNOTE_RECOMMEND_CLOSE': (datetime.datetime(2020, 5, 1, tzinfo=KST), '키노트 연사 추천 종료'),
    'LIGHTNING_TALK_OPEN': (datetime.datetime(2020, 9, 1, tzinfo=KST), '라이트닝 토크 모집 오픈'),
    'LIGHTNING_TALK_CLOSE': (datetime.datetime(2020, 9, 1, tzinfo=KST), '라이트닝 토크 모집 종료'),
    'LIGHTNING_TALK_N': (10, '라이트닝 토크 접수 제한'),
    'PROGRAM_OPEN': (datetime.datetime(2020, 8, 26, tzinfo=KST), '발표 목록 공개'),
    'SCHEDULE_OPEN': (datetime.datetime(2020, 9, 1, tzinfo=KST), '발표 시간표 공개'),
    'KEYNOTE_OPEN': (datetime.datetime(2020, 9, 1, tzinfo=KST), '키노트 연사 공개'),
    'TICKET_OPEN': (datetime.datetime(2020, 8, 1, tzinfo=KST), '티켓 판매 시작'),
    'TICKET_CLOSE': (datetime.datetime(2020, 9, 28, tzinfo=KST), '티켓 판매 종료'),
    'PATRON_OPEN': (datetime.datetime(2020, 8, 1, tzinfo=KST), '개인 후원 티켓 판매 시작'),
    'PATRON_CLOSE': (datetime.datetime(2020, 9, 28, tzinfo=KST), '개인 후원 티켓 판매 종료'),
    'PATRON_URL': ('', '개인 후원 티켓 판매 URL'),
    'YOUTUBE_TRACK_1': ('', '트랙1 YouTube 링크'),
    'YOUTUBE_TRACK_2': ('', '트랙2 YouTube 링크'),
    'YOUTUBE_TRACK_3': ('', '트랙3 YouTube 링크'),
    'YOUTUBE_TRACK_4': ('', '트랙4 YouTube 링크'),
    'YOUTUBE_TRACK_5': ('', '트랙5 YouTube 링크'),
    'YOUTUBE_TRACK_LT_1': ('', '토요일 라이트닝 토크 YouTube 링크'),
    'YOUTUBE_TRACK_LT_2': ('', '일요일 라이트닝 토크 YouTube 링크'),
    'YOUTUBE_TRACK_CLOSING': ('', '클로징 YouTube 링크'),
    'SLACK_INVITATION_OPEN': (datetime.datetime(2020, 9, 25, tzinfo=KST), '참가자 슬랙 초대 시작'),
    'SLACK_INVITATION_CLOSE': (datetime.datetime(2020, 9, 27, tzinfo=KST), '참가자 슬랙 초대 종료'),
}

CONSTANCE_CONFIG_FIELDSETS = {
    'SLACK': ('SLACK_CHANNEL', 'CFS_NOTI_CHANNEL', 'SLACK_INVITATION_ALARM_CHANNEL', 'SLACK_TOKEN'),
    'Ticket': ('TICKET_OPEN', 'TICKET_CLOSE', 'PATRON_OPEN', 'PATRON_CLOSE',),
    'Program': ('CFP_OPEN', 'CFP_CLOSE', 'OPEN_REVIEW_START', 'OPEN_REVIEW_FINISH',
                'KEYNOTE_RECOMMEND_OPEN', 'KEYNOTE_RECOMMEND_CLOSE', 'LIGHTNING_TALK_OPEN',
                'LIGHTNING_TALK_CLOSE', 'LIGHTNING_TALK_N', 'PROGRAM_OPEN', 'SCHEDULE_OPEN', 'KEYNOTE_OPEN',
                'PROGRAM_DETAIL_EDITABLE'),
    'Sponsor': ('CFS_OPEN', 'CFS_CLOSE', 'VIRTUAL_BOOTH_EDITABLE', 'VIRTUAL_BOOTH_EDIT_FINISH', 'VIRTUAL_BOOTH_OPEN',),
    'Template': ('CFP_BRIEF_TEMPLATE', 'CFP_DESC_TEMPLATE',),
    'Etc.': ('TOTAL_TICKET', 'PATRON_URL', 'YOUTUBE_TRACK_1', 'YOUTUBE_TRACK_2', 'YOUTUBE_TRACK_3', 'YOUTUBE_TRACK_4',
             'YOUTUBE_TRACK_5', 'YOUTUBE_TRACK_LT_1', 'YOUTUBE_TRACK_LT_2', 'YOUTUBE_TRACK_CLOSING',
             'SLACK_INVITATION_OPEN', 'SLACK_INVITATION_CLOSE'),
}

# For supporting i18n of django modules
MIGRATION_MODULES = {
    'flatpages': 'pyconkr.flatpages_migrations',
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            # 'filters': ['require_debug_true'], # 임시
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'stream': sys.stdout
        },
    },
    'loggers': {
        'django': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': True,
        },
    }
}

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
    'compressor.finders.CompressorFinder',
]

# https://blog.jaeyoon.io/2017/10/django-sass.html
SASS_PROCESSOR_ENABLED = True
SASS_PROCESSOR_AUTO_INCLUDE = False

SASS_PROCESSOR_INCLUDE_FILE_PATTERN = r'^.+\.scss$'

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

# django debugger toolbar
INTERNAL_IPS = ['127.0.0.1', ]
INTERNAL_IPS += [os.getenv('DEBUG_IP1')]
