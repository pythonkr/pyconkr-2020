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
    list_display = ('id', 'slug', 'name',)
    ordering = ('name',)
    list_editable = ('slug', 'name',)
    search_fields = ('name',)


admin.site.register(Sponsor, SponsorAdmin)


class SponsorLevelAdmin(SummernoteModelAdmin, TranslationAdmin):
    list_display = ('id', 'order', 'name', 'slug',)
    list_editable = ('order', 'name', 'slug',)
    ordering = ('order',)
    search_fields = ('name',)


admin.site.register(SponsorLevel, SponsorLevelAdmin)
