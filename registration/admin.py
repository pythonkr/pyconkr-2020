# -*- coding: utf-8 -*-
from django.contrib import admin
from registration.models import Ticket


class TicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_patron')


admin.site.register(Ticket, TicketAdmin)
