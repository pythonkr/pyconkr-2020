from django.contrib import admin
from mailing.models import Mailing, NewsLetter


class MailingAdmin(admin.ModelAdmin):
    list_display = ('title', 'send_now', 'send_datetime', 'send_to_all_participant',
                    'send_to_newsletter_subscriber', 'send_yn',)


admin.site.register(Mailing, MailingAdmin)


class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ('email_address',)


admin.site.register(NewsLetter, NewsLetterAdmin)
