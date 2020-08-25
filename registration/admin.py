# -*- coding: utf-8 -*-
from django.contrib import admin
from registration.models import Ticket
from import_export.admin import ImportExportModelAdmin


class TicketAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('user', 'is_patron', 'price',)
    list_filter = ('is_patron',)
    autocomplete_fields = ('user',)
    actions = ('to_patron',)

    def to_patron(self, request, queryset):
        queryset.update(is_patron=True)

    to_patron.short_description = "개인 후원으로 지정합니다."


admin.site.register(Ticket, TicketAdmin)
