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
from .models import (Room, Program, ProgramTime, ProgramDate, ProgramCategory,
                     Speaker, Preference, Proposal, TutorialProposal, SprintProposal,
                     TutorialCheckin, SprintCheckin, OpenReview, LightningTalk)


class RoomAdmin(SummernoteModelAdmin, TranslationAdmin):
    list_display = ('id', 'name',)
    list_editable = ('name',)
    search_fields = ('name',)


# admin.site.register(Room, RoomAdmin)


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
    list_display = ('id', 'name', 'date', 'room', 'slide_url',
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


class ProposalAdmin(ImportMixin, admin.ModelAdmin):
    form = ProposalAdminForm
    list_display = ('id', 'user', 'title', 'difficulty', 'duration', 'language', 'category',)


admin.site.register(Proposal, ProposalAdmin)


class TutorialProposalAdminForm(forms.ModelForm):
    class Meta:
        model = TutorialProposal
        fields = '__all__'
        widgets = {
            'desc': SummernoteWidgetWithCustomToolbar(),
            'comment': SummernoteWidgetWithCustomToolbar(),
        }


class TutorialProposalAdmin(admin.ModelAdmin):
    form = TutorialProposalAdminForm
    list_display = ('user', 'title', 'difficulty', 'duration', 'language', 'capacity',
                    'begin_date', 'begin_time', 'end_date', 'end_time',)


# admin.site.register(TutorialProposal, TutorialProposalAdmin)


class SprintProposalAdminForm(forms.ModelForm):
    class Meta:
        model = SprintProposal
        fields = '__all__'
        widgets = {
            'contribution_desc': SummernoteWidgetWithCustomToolbar(),
            'comment': SummernoteWidgetWithCustomToolbar(),
        }


class SprintProposalAdmin(admin.ModelAdmin):
    form = SprintProposalAdminForm
    list_display = ('title', 'language', 'project_url',
                    'project_brief', 'contribution_desc')


# admin.site.register(SprintProposal, SprintProposalAdmin)


class TutorialCheckinAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tutorial',)


# admin.site.register(TutorialCheckin, TutorialCheckinAdmin)


class SprintCheckinAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'sprint',)


# admin.site.register(SprintCheckin, SprintCheckinAdmin)

class OpenReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'submitted',)
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
