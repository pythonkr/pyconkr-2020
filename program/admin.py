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
from .models import ProgramCategory, Proposal, OpenReview, LightningTalk


class ProgramCategoryAdmin(TranslationAdmin, ImportExportModelAdmin):
    list_display = ('id', 'name', 'slug', 'visible')


admin.site.register(ProgramCategory, ProgramCategoryAdmin)


class ProposalAdminForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = '__all__'
        widgets = {
            'desc': SummernoteWidgetWithCustomToolbar(),
            'comment': SummernoteWidgetWithCustomToolbar(),
            'introduction': SummernoteWidgetWithCustomToolbar(),
        }


class ProposalAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    form = ProposalAdminForm
    list_display = ('id', 'user', 'title', 'difficulty', 'duration', 'language', 'category', 'accepted',)
    list_filter = ('accepted',)


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
