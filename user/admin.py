from mail_templated import send_mail
import random
import string
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from sorl.thumbnail.admin import AdminImageMixin
from .models import Profile, Staff

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
    parameter_name = "user_code"

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


class ProfileImageListFilter(admin.SimpleListFilter):
    title = "Profile image"
    parameter_name = "image_ori"

    def lookups(self, request, model_admin):
        return (
            ('empty', 'Empty'),
            ('exist', 'Not empty'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'empty':
            return queryset.filter(image_ori__isnull=True)
        if self.value() == 'exist':
            return queryset.filter(image_ori__isnull=False)


class ProfileSmallImageListFilter(admin.SimpleListFilter):
    title = "Small image"
    parameter_name = "image_small"

    def lookups(self, request, model_admin):
        return (
            ('empty', 'Empty'),
            ('exist', 'Not empty'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'empty':
            return queryset.filter(image_small__isnull=True)
        if self.value() == 'exist':
            return queryset.filter(image_small__isnull=False)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name_ko', 'name_en', 'user_code', 'image_ori', 'image_small',)
    list_filter = (UserCodeListFilter, ProfileImageListFilter, ProfileSmallImageListFilter,)
    search_fields = ('user__username', 'user_code', 'name_ko', 'name_en',)
    actions = ('make_user_code', 'make_small_image',)

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

    def make_small_image(self, request, queryset):
        for p in queryset:
            if p.image_small:
                continue
            image = p.image_ori
            small_image_size = 256
            new_width = 0
            new_height = 0
            if image.width >= image.height:
                new_height = small_image_size
                new_width = int(small_image_size * image.width / image.height)
            else:
                new_width = small_image_size
                new_height = int(small_image_size * image.height / image.width)

            try:
                PIL_image = Image.open(image.file)
                image_small = PIL_image.resize((new_width, new_height))
                blob = BytesIO()
                image_small.save(blob, 'PNG')
                p.image_small.save(image.name + '_small.jpg', File(blob), save=False)
                p.save()
            except ValueError:
                pass


# admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)


class StaffAdmin(admin.ModelAdmin):
    list_display = ('name_ko', 'name_en', 'user',)
    autocomplete_fields = ('user',)
    ordering = ('name_ko',)


admin.site.register(Staff, StaffAdmin)
