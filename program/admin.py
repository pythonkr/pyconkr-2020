from django import forms
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from pyconkr.admin import SummernoteWidgetWithCustomToolbar
from modeltranslation.admin import TranslationAdmin
from sorl.thumbnail.admin import AdminImageMixin
from import_export.admin import ImportExportModelAdmin
from .models import ProgramCategory, Proposal, OpenReview, LightningTalk, Sprint


class ProgramCategoryAdmin(TranslationAdmin, ImportExportModelAdmin):
    list_display = ('id', 'name', 'slug', 'visible',)


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
    list_display = ('id', 'user', 'title', 'accepted', 'category', 'video_open_at', 'track_num',)
    list_filter = ('accepted',)
    autocomplete_fields = ('user',)
    actions = ('to_track1', 'to_track2', 'to_track3',)

    def to_track1(self, request, queryset):
        queryset.update(track_num=1)

    to_track1.short_description = "트랙 1번으로 설정"

    def to_track2(self, request, queryset):
        queryset.update(track_num=2)

    to_track2.short_description = "트랙 2번으로 설정"

    def to_track3(self, request, queryset):
        queryset.update(track_num=3)

    to_track3.short_description = "트랙 3번으로 설정"


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
    list_display = ('owner', 'title', 'day', 'accepted', 'created_at',)


admin.site.register(LightningTalk, LightningTalkAdmin)


class SprintAdmin(admin.ModelAdmin):
    list_display = ('creator', 'title', 'language', 'url',)


admin.site.register(Sprint, SprintAdmin)
