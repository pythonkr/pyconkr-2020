# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

EVENT_CONFERENCE = 'conference'
EVENT_TUTORIAL = 'tutorial'
EVENT_YOUNG = 'youngcoder'
EVENT_BABYCARE = 'babycare'
EVENT_TYPES = (
    (EVENT_CONFERENCE, '컨퍼런스',),
    (EVENT_TUTORIAL, '튜토리얼',),
    (EVENT_YOUNG, '영코더',),
    (EVENT_BABYCARE, '아이돌봄',),
)

CONFERENCE_REGISTRATION_EARLYBIRD = 'earlybird'
CONFERENCE_REGISTRATION_REGULAR = 'regular'
CONFERENCE_REGISTRATION_COMPANY = 'company'
CONFERENCE_REGISTRATION_PATRON = 'patron'
CONFERENCE_REGISTRATION_TYPES = (
    (CONFERENCE_REGISTRATION_EARLYBIRD, '얼리버드',),
    (CONFERENCE_REGISTRATION_REGULAR, '일반',),
    (CONFERENCE_REGISTRATION_COMPANY, '법인',),
    (CONFERENCE_REGISTRATION_PATRON, '개인후원',),
)

