from django.contrib import admin
from django.db import models

from mailing.models import Mailing, NewsLetter

from pyconkr.admin import SummernoteWidgetWithCustomToolbar


class MailingAdmin(admin.ModelAdmin):
    list_display = ('title', 'send_datetime', 'send_to',
                    'send_to_newsletter_subscriber', 'send_successfully')
    readonly_fields = ('send_successfully',)
    formfield_overrides = {models.TextField: {
        'widget': SummernoteWidgetWithCustomToolbar}}


admin.site.register(Mailing, MailingAdmin)


class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ('email_address', 'agree_coc',)
    list_filter = ('agree_coc',)


admin.site.register(NewsLetter, NewsLetterAdmin)
