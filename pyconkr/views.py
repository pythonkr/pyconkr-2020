# -*- coding: utf-8 -*-
from mail_templated import send_mail
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import social_account_added
from django.contrib.auth import login as user_login, logout as user_logout
from django.contrib.auth import get_user_model
from django import template
from django.urls import reverse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.views.generic import ListView
from announcement.models import Announcement
from registration.models import Registration, Option, CONFERENCE_REGISTRATION_PATRON
from django.utils.translation import get_language, activate

User = get_user_model()


def index(request):
    return render(request, 'index.html', {
        'index': True,
        'recent_announcements': Announcement.objects.all()[:3],
    })


class PatronList(ListView):
    model = Registration
    template_name = "pyconkr/patron_list.html"

    def get_queryset(self):
        queryset = super(PatronList, self).get_queryset()
        patron_option = Option.objects.filter(
            conference_type=CONFERENCE_REGISTRATION_PATRON)

        if patron_option.exists():
            return queryset.filter(option__in=patron_option, payment_status='paid').order_by('-additional_price', 'created')

        return None


def robots(request):
    http_host = request.get_host()
    if http_host is not None and http_host.startswith("dev.pycon.kr"):
        return render(request, 'dev-robots.txt', content_type='text/plain')
    return render(request, 'robots.txt', content_type='text/plain')


def login(request):
    if request.user.is_authenticated:
        return redirect('profile')

    return render(request, 'login.html', {
        'title': _('Login'),
    })


def logout(request):
    user_logout(request)
    return redirect(reverse('index'))


@receiver(user_signed_up)
def user_signed_up_custom(request, user, **kwargs):
    from_email = 'PyCon Korea <pyconkr@pycon.kr>'
    email = user.email
    if not email:
        return
    send_mail('mail/welcome.html', {'user': user}, from_email, [email])
