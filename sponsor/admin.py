from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib.flatpages.models import FlatPage
from django.db import models
from django_summernote.admin import SummernoteModelAdmin
from django_summernote.widgets import SummernoteWidget
from modeltranslation.admin import TranslationAdmin
from sorl.thumbnail.admin import AdminImageMixin
from .models import (Sponsor, SponsorLevel)
from pyconkr.admin import SummernoteWidgetWithCustomToolbar


class SponsorAdmin(SummernoteModelAdmin, TranslationAdmin):
    formfield_overrides = {models.TextField: {
        'widget': SummernoteWidgetWithCustomToolbar}}
    list_display = ('creator', 'name', 'slug', 'level', 'manager_name', 'manager_email',
                    'submitted', 'accepted', 'paid_at', 'created_at')
    ordering = ('-created_at',)
    list_editable = ('slug',)
    search_fields = ('name',)


admin.site.register(Sponsor, SponsorAdmin)


class SponsorLevelAdmin(SummernoteModelAdmin, TranslationAdmin):
    list_display = ('id', 'order', 'name', 'slug', 'price', 'limit',)
    list_editable = ('order', 'slug',)
    ordering = ('order',)
    search_fields = ('name',)


admin.site.register(SponsorLevel, SponsorLevelAdmin)
