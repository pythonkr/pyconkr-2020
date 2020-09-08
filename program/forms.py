from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django import forms
from django.forms import ModelChoiceField, ChoiceField
from django_summernote.widgets import SummernoteInplaceWidget
from django.shortcuts import reverse
from django.utils.translation import ugettext_lazy as _
from .models import Proposal, OpenReview, ProgramCategory, LightningTalk

from constance import config


class ProposalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProposalForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', _('Submit')))

        self.fields['brief'].initial = config.CFP_BRIEF_TEMPLATE
        self.fields['desc'].initial = config.CFP_DESC_TEMPLATE
        self.fields['category'].queryset = ProgramCategory.objects.filter(visible=True)

    class Meta:
        model = Proposal
        fields = ('title', 'brief', 'desc', 'comment',
                  'difficulty', 'duration', 'language', 'category',)
        widgets = {
            'desc': SummernoteInplaceWidget(),
            'comment': SummernoteInplaceWidget(),
        }
        labels = {
            'title': _('Proposal title (required)'),
            'brief': _('Brief (required)'),
            'desc': _('Detailed description (required)'),
            'comment': _('Comment to reviewers (optional)'),
            'difficulty': _('Session difficulty'),
            'duration': _('Session duration'),
            'language': _('Session language'),
            'category': _('Category'),
        }


class CategoryChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.name}'


class LanguageChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj}'


class OpenReviewLanguageForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(OpenReviewLanguageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('next', _('Next')))
        self.fields['language'] = ChoiceField(choices=(
            ('N', '상관 없음'),
            ('K', '한국어'),
            ('E', 'English'),
        ), help_text=_('어떤 언어로 작성된 발표 제안을 리뷰할지 선택하세요.'))

    class Meta:
        fields = ('language',)
        labels = {
            'language': _('언어'),
        }


class OpenReviewCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OpenReviewCategoryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('next', _('Next')))
        self.fields['category'] = CategoryChoiceField(label=_('카테고리'),
                                                      queryset=ProgramCategory.objects.filter(visible=True).exclude(
                                                          proposal=None),
                                                      help_text=_('리뷰할 분야를 선택하세요. 발표 제안이 없는 분야는 표시되지 않습니다.')
                                                      )
        # 이전 폼에서 선택한 언어정보 저장용 Hidden input 생성 (View에서 helper를 이용해 추가)

    class Meta:
        model = OpenReview
        fields = ('category',)
        labels = {
            'category': _('카테고리 이름'),
        }


class OpenReviewCommentForm(forms.ModelForm):
    comment = forms.CharField(min_length=20, max_length=2000, widget=forms.Textarea())

    def __init__(self, *args, **kwargs):
        super(OpenReviewCommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('save', _('Save')))

    class Meta:
        model = OpenReview
        fields = ('comment',)
        labels = {
            'comment': _('Comment')
        }


class LightningTalkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LightningTalkForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', _('Submit')))
        LT_N = config.LIGHTNING_TALK_N
        if len(LightningTalk.objects.filter(day=1)) >= LT_N:
            if len(LightningTalk.objects.filter(day=2)) < LT_N:
                self.fields['day'] = ChoiceField(choices=((2, _('일요일')),))
        else:
            if len(LightningTalk.objects.filter(day=2)) < LT_N:
                self.fields['day'] = ChoiceField(choices=((1, _('토요일')), (2, _('일요일')),))
            else:
                self.fields['day'] = ChoiceField(choices=((1, _('토요일')),))
        self.fields['video_url'].required = True

    class Meta:
        model = LightningTalk
        fields = ('title', 'video_url', 'slide_url', 'day', 'brief', 'comment',)
        labels = {
            'title': _('발표 제목'),
            'video_url': _('발표 영상 URL'),
            'slide_url': _('발표 슬라이드 URL'),
            'day': _('발표 요일'),
            'brief': _('발표 소개 문구'),
            'comment': _('준비위원회에게 남기고 싶은 말'),
        }


class ProgramUpdateForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ('title', 'introduction', 'slide_url',)
        labels = {
            'title': _('Proposal title (required)'),
            'introduction': _('발표 소개 문구'),
            'slide_url': _('발표 자료 URL'),
        }
        widgets = {
            'introduction': SummernoteInplaceWidget(),
        }

    def __init__(self, *args, **kwargs):
        super(ProgramUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', _('Submit')))
