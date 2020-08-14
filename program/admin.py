from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib.flatpages.models import FlatPage
from django.db import models
from django_summernote.admin import SummernoteModelAdmin
from pyconkr.admin import SummernoteWidgetWithCustomToolbar
from modeltranslation.admin import TranslationAdmin
from sorl.thumbnail.admin import AdminImageMixin
from import_export.admin import ImportExportModelAdmin, ImportMixin
from .models import (Program, ProgramTime, ProgramDate, ProgramCategory,
                     Speaker, Preference, Proposal, OpenReview, LightningTalk)


class ProgramDateAdmin(admin.ModelAdmin):
    list_display = ('id', 'day',)


# admin.site.register(ProgramDate, ProgramDateAdmin)


class ProgramTimeAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'begin', 'end', 'day')
    list_editable = ('name', 'day')
    ordering = ('begin',)


# admin.site.register(ProgramTime, ProgramTimeAdmin)


class ProgramCategoryAdmin(TranslationAdmin, ImportExportModelAdmin):
    list_display = ('id', 'name', 'slug', 'visible')


admin.site.register(ProgramCategory, ProgramCategoryAdmin)


class ProgramAdmin(SummernoteModelAdmin, TranslationAdmin):
    list_display = ('id', 'name', 'date', 'slide_url',
                    'pdf_url', 'get_speakers', 'category', 'is_recordable',)
    list_editable = ('name', 'category', 'is_recordable',)
    ordering = ('id',)
    filter_horizontal = ('times',)
    search_fields = ('name', 'speakers__name', 'desc',)


admin.site.register(Program, ProgramAdmin)


class PreferenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'program',)


# admin.site.register(Preference, PreferenceAdmin)


class ProposalAdminForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = '__all__'
        widgets = {
            'desc': SummernoteWidgetWithCustomToolbar(),
            'comment': SummernoteWidgetWithCustomToolbar(),
        }


class ProposalAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    form = ProposalAdminForm
    list_display = ('id', 'user', 'title', 'difficulty', 'duration', 'language', 'category',)


admin.site.register(Proposal, ProposalAdmin)


class OpenReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'category', 'submitted',)
    list_filter = ('submitted',)

    def title(self, obj):
        return obj.proposal.title

    def user(self, obj):
        return obj.user.name


admin.site.register(OpenReview, OpenReviewAdmin)


class LightningTalkAdminForm(forms.ModelForm):
    class Meta:
        model = LightningTalk
        fields = '__all__'


class LightningTalkAdmin(admin.ModelAdmin):
    form = LightningTalkAdminForm
    list_display = ('owner', 'title', 'day', 'accepted', 'created_at')


admin.site.register(LightningTalk, LightningTalkAdmin)
