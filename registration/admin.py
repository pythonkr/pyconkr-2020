# -*- coding: utf-8 -*-
from django.contrib import admin
from registration.models import Ticket
from import_export.admin import ImportExportModelAdmin


class TicketAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('user', 'is_patron', 'price', 'agree_coc', 'get_user_code', 'get_user_email',)
    list_filter = ('is_patron', 'agree_coc',)
    search_fields = ('user__profile__user_code', 'user__email',)
    autocomplete_fields = ('user',)
    actions = ('to_patron', 'to_agree_coc',)

    def to_patron(self, request, queryset):
        queryset.update(is_patron=True)

    to_patron.short_description = "개인 후원으로 지정합니다."

    def to_agree_coc(self, request, queryset):
        queryset.update(agree_coc=True)

    to_agree_coc.short_description = "CoC에 동의한 것으로 합니다."

    def get_user_code(self, obj):
        return obj.user.profile.user_code

    get_user_code.short_description = "User code"

    def get_user_email(self, obj):
        return obj.user.email

    get_user_email.short_description = "User email"


admin.site.register(Ticket, TicketAdmin)
