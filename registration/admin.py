# -*- coding: utf-8 -*-
from django.contrib import admin
from registration.models import Ticket
from import_export.admin import ImportExportModelAdmin


class TicketAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('user', 'is_patron', 'price',)
    list_filter = ('is_patron',)


admin.site.register(Ticket, TicketAdmin)
