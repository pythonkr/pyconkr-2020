# -*- coding: utf-8 -*-
import datetime

from constance import config
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, TemplateView, ListView
from django.http import HttpResponseForbidden

from .models import Ticket

from user.models import Profile

KST = datetime.timezone(datetime.timedelta(hours=9))


class RegistrationHome(TemplateView):
    template_name = 'registration/registration_buy_ticket.html'

    def get(self, request, *args, **kwargs):

        # 티켓 구매 가능 기간 검증
        ticket_open = config.TICKET_OPEN.astimezone(KST)
        ticket_close = config.TICKET_CLOSE.astimezone(KST)
        now = datetime.datetime.now(tz=KST)

        if not (ticket_open < now < ticket_close):
            return HttpResponseForbidden()

        # 기 구매자 예외 처리
        if Ticket.objects.filter(user=request.user).exists() and Ticket.objects.get(user=request.user).agree_coc:
            return redirect('profile')

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # 요청 유효성 검증
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        # CoC 검증
        if request.POST.get('coc') is None:
            return HttpResponseForbidden()

        # 메일링 동의 갱신
        if request.POST.get('mailing') == 'true':
            req_user_profile = Profile.objects.get(user=request.user)
            req_user_profile.agreement_receive_advertising_info = True
            req_user_profile.save()

        if Ticket.objects.filter(user=request.user).exists():
            ticket = Ticket.objects.get(user=request.user)
            ticket.agree_coc = True
            ticket.save()
        else:
            # 신규 티켓 등록
            new_ticket = Ticket()
            new_ticket.user = request.user
            new_ticket.agree_coc = True
            new_ticket.save()

        return redirect('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 요청한 사용자의 메일링 수신 동의여부 확인
        req_user_profile = Profile.objects.get(user=self.request.user)

        if req_user_profile.agreement_receive_advertising_info is True:
            context['checked'] = 'checked'
        else:
            context['checked'] = ''

        return context


class TicketList(TemplateView):
    template_name = 'registration/ticket_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 티켓 구매 가능 기간 검증
        ticket_open = config.TICKET_OPEN.astimezone(KST)
        ticket_close = config.TICKET_CLOSE.astimezone(KST)
        patron_open = config.PATRON_OPEN.astimezone(KST)
        patron_close = config.PATRON_CLOSE.astimezone(KST)
        now = datetime.datetime.now(tz=KST)

        if now < ticket_open:
            context['ticket_available'] = -1
        elif ticket_open < now < ticket_close:
            context['ticket_available'] = 0
        else:
            context['ticket_available'] = 1

        if now < patron_open:
            context['patron_available'] = -1
        elif patron_open < now < patron_close:
            context['patron_available'] = 0
        else:
            context['patron_available'] = 1

        # 기구매 티켓 확인
        context['already_buy'] = False
        if self.request.user.is_authenticated and Ticket.objects.filter(user=self.request.user).exists():
            context['already_buy'] = True

        context['patron_url'] = config.PATRON_URL

        return context


class PatronList(ListView):
    template_name = 'pyconkr/patron_list.html'
    queryset = Ticket.objects.filter(is_patron=True)
    ordering = ('-price',)
