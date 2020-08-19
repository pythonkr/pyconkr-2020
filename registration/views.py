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
from django.http import HttpResponseForbidden

from pyconkr.helper import render_io_error
from program.models import Speaker
from .models import EVENT_CONFERENCE, EVENT_YOUNG, EVENT_BABYCARE, EVENT_TUTORIAL, Ticket

from user.models import Profile

KST = datetime.timezone(datetime.timedelta(hours=9))


class RegistrationHome(TemplateView):
    template_name = 'registration/registration_buy_ticket.html'

    def get(self, request, *args, **kwargs):

        # 티켓 구매 가능 기간 검증
        ticket_open = config.CFS_OPEN.astimezone(KST)
        ticket_close = config.CFS_CLOSE.astimezone(KST)
        now = datetime.datetime.now(tz=KST)

        if not (ticket_open < now < ticket_close):
            return HttpResponseForbidden()

        # 기 구매자 예외처리
        if Ticket.objects.filter(user=request.user):
            return redirect('profile')

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # 요청 유효성 검증
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        # CoC 검증
        if request.POST['coc_agreement'] == '0':    # 필요시 키 수정
            return HttpResponseForbidden()

        # 메일링 동의 갱신
        req_user_profile = Profile.objects.get(user=request.user)
        req_user_profile.agreement_receive_advertising_info = request.POST['mailing_agreement']     # 필요시 키 수정
        req_user_profile.save()

        # 신규 티켓 등록
        new_ticket = Ticket()
        new_ticket.user = request.user
        new_ticket.ticket_purchase_datetime = datetime.datetime.now()
        new_ticket.save()

        return redirect('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 요청한 사용자의 메일링 수신 동의여부 확인
        req_user_profile = Profile.objects.get(user=self.request.user)
        context['mailing_agreement'] = req_user_profile.agreement_receive_advertising_info

        return context


class TicketList(TemplateView):
    template_name = 'registration/ticket_list.html'
