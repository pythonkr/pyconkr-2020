# -*- coding: utf-8 -*-
import datetime
from uuid import uuid4

import pytz
from constance import config
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView

from pyconkr.helper import render_io_error
from program.models import Speaker
from .models import EVENT_CONFERENCE, EVENT_YOUNG, EVENT_BABYCARE, EVENT_TUTORIAL

