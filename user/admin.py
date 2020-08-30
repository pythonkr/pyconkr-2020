from mail_templated import send_mail
import random, string
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from sorl.thumbnail.admin import AdminImageMixin
from .models import Profile

User = get_user_model()


def send_test_mail(modeladmin, request, queryset):
    from_email = 'PyCon Korea <pyconkr@pycon.kr>'
    for obj in queryset:
        email = obj.email
        if not email:
            continue
        print(f'sent {email}')
        send_mail('mail/test.html', {'user': obj}, from_email, [email])


send_test_mail.short_description = 'Send test mail'


class ProfileInline(AdminImageMixin, admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    actions = (send_test_mail,)


class UserCodeListFilter(admin.SimpleListFilter):
    title = "User code"
    parameter_name = "empty"

    def lookups(self, request, model_admin):
        return (
            ('empty', 'Empty'),
            ('filled', 'Not empty'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'empty':
            return queryset.filter(user_code=None)
        if self.value() == 'filled':
            return queryset.filter(user_code__regex='.*')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name_ko', 'name_en', 'user_code',)
    list_filter = (UserCodeListFilter,)
    search_fields = ('user_code',)
    actions = ('make_user_code',)

    def make_user_code(self, request, queryset):
        length = 20
        pool = string.ascii_letters + string.digits

        for p in queryset:
            if p.user_code:
                continue
            while True:
                result = ""
                for _ in range(length):
                    result += random.choice(pool)

                if not Profile.objects.filter(user_code=result).exists():
                    break

            p.user_code = result
            p.save()


# admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
