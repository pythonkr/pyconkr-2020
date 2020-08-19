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
from django.views.generic import DetailView, TemplateView

from pyconkr.helper import render_io_error
from program.models import Speaker
from .models import EVENT_CONFERENCE, EVENT_YOUNG, EVENT_BABYCARE, EVENT_TUTORIAL, Ticket


class RegistrationHome(TemplateView):
    template_name = 'registration/registration_buy_ticket.html'

    def get(self, request, *args, **kwargs):

        # 기 구매자 예외처리
        if Ticket.objects.filter(user=request.user):
            return redirect('profile')

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        new_ticket = Ticket()

        if request.user.is_authenticated:
            new_ticket.user = request.user
            new_ticket.ticket_purchase_datetime = datetime.datetime.now()
            new_ticket.save()
        else:
            return HttpResponse(status=401)     # UnAuthorize

        return redirect('profile')

    def get_context_data(self, **kwargs):
        print('get_context_data')
        return super().get_context_data(**kwargs)


class TicketList(TemplateView):
    template_name = 'registration/ticket_list.html'
