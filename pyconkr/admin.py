from import_export.admin import ImportExportMixin, ImportExportModelAdmin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.flatpages.models import FlatPage
from django.db import models
from django_summernote.admin import SummernoteModelAdmin
from django_summernote.widgets import SummernoteWidget
from modeltranslation.admin import TranslationAdmin
from .models import (EmailToken, Banner)
from import_export import resources


class SummernoteWidgetWithCustomToolbar(SummernoteWidget):
    def template_contexts(self):
        contexts = super(SummernoteWidgetWithCustomToolbar,
                         self).template_contexts()
        contexts['width'] = '960px'
        return contexts


class EmailTokenAdmin(admin.ModelAdmin):
    list_display = ('email', 'token', 'created')
    search_fields = ('email',)


# admin.site.register(EmailToken, EmailTokenAdmin)


class FlatPageResource(resources.ModelResource):

    class Meta:
        model = FlatPage


class FlatPageAdmin(TranslationAdmin, ImportExportModelAdmin):
    formfield_overrides = {models.TextField: {
        'widget': SummernoteWidgetWithCustomToolbar}}
    resource_class = FlatPageResource


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)


class BannerAdmin(SummernoteModelAdmin, TranslationAdmin):
    list_display = ('id', 'name', 'url', 'begin', 'end')
    ordering = ('id',)
    search_fields = ('name', 'url')


# admin.site.register(Banner, BannerAdmin)
