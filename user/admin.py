from mail_templated import send_mail
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
        send_mail('email_extras/test.html', {'user': obj}, from_email, [email])


send_test_mail.short_description = 'Send test mail'


class ProfileInline(AdminImageMixin, admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )
    actions = (send_test_mail,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
