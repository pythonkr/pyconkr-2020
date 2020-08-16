# -*- coding: utf-8 -*-
from constance import config
from django.contrib import admin
from django.core.mail import send_mass_mail
from django.shortcuts import render
from django.utils import timezone

from registration.models import Ticket


class TicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_patron')


admin.site.register(Ticket, TicketAdmin)
