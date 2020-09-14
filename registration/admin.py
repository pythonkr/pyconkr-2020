# -*- coding: utf-8 -*-
from django.contrib import admin
from registration.models import Ticket, Patron
from user.models import Profile
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


class PatronAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('user_code', 'price',)
    search_fields = ('user_code',)
    actions = ('to_ticket',)

    def to_ticket(self, request, queryset):
        for p in queryset:
            user = Profile.objects.get(user_code=p.user_code).user
            if Ticket.objects.filter(user=user).exists():
                ticket = Ticket.objects.get(user=user)
                if not ticket.is_patron:
                    ticket.is_patron = True
                    ticket.price = p.price
                    ticket.save()
                    p.delete()
                else:
                    if ticket.price == p.price:
                        p.delete()
            else:
                ticket = Ticket(user=user, is_patron=True, price=p.price)
                ticket.save()
                p.delete()

    to_ticket.short_description = "Make a patron ticket"


admin.site.register(Patron, PatronAdmin)
