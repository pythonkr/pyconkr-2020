# -*- coding: utf-8 -*-
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


# @register.simple_tag(takes_context=True)
# def change_lang(context, lang=None, *args, **kwargs):
#     """
#     Get active page's url by a specified language
#     Usage: {% change_lang 'en' %}
#     """
#     path = context['request'].path
#     full_path = context['request'].get_full_path()
#     try:
#         url_parts = resolve(path)
#         cur_language = get_language()
#         try:
#             activate(lang)
#             url = reverse(url_parts.view_name, kwargs=url_parts.kwargs)
#             activate(cur_language)
#             parameters = "?{0}".format(full_path.split('?')[1]) if len(
#                 full_path.split('?')) == 2 else ""
#             return "{0}{1}".format(url, parameters)
#         except Exception:
#             pass
#     except Exception:
#         pass
#     return full_path
