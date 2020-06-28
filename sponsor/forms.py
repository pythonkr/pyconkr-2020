from django.shortcuts import reverse
from django import forms
from django_summernote.widgets import SummernoteInplaceWidget
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Sponsor, SponsorLevel

from django.forms import ModelChoiceField


class SponsorLevelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        if obj.current_remaining_number == 0:
            return "{name} ({msg})".format(name=obj.name, msg=_("마감"))
        return f'{obj.name} ({obj.current_remaining_number}/{obj.limit})'


class SponsorForm(forms.ModelForm):
    class Meta:
        model = Sponsor
        fields = ('name_ko', 'name_en', 'level', 'manager_name', 'manager_email',
                  'business_registration_number', 'business_registration_file',
                  'url', 'logo_image', 'desc_ko', 'desc_en',)
        widgets = {
            'desc_ko': SummernoteInplaceWidget(),
            'desc_en': SummernoteInplaceWidget(),
        }
        labels = {
            'level': _('후원사 등급'),
            'logo_image': _('로고 이미지'),
            'name_ko': _('후원사 이름 (한글)'),
            'name_en': _('후원사 이름 (영문)'),
            'url': _('후원사 홈페이지 주소'),
            'desc_ko': _('후원사 소개 (한글)'),
            'desc_en': _('후원사 소개 (영문)'),
            'manager_name': _('후원 담당자 이름'),
            'manager_email': _('후원 담당자 이메일'),
            'business_registration_number': _('후원사 사업자 등록 번호'),
            'business_registration_file': _('후원사 사업자 등록증'),
        }

    def __init__(self, *args, **kwargs):
        super(SponsorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        # 제출 버튼은 View에서 추가 (저장, 제출 버튼 분리 목적)

        self.fields['name_ko'].required = True
        self.fields['name_en'].required = True
        self.fields['level'] = SponsorLevelChoiceField(label=_('후원사 등급'),
                                                       queryset=SponsorLevel.objects.filter(visible=True),
                                                       help_text=_('후원을 원하시는 등급을 선택해주십시오. 모두 판매된 등급은 선택할 수 없습니다.'))

    def form_valid(self, form):
        if self.request.POST['submit'] == 'save':
            return super(SponsorForm, self).form_valid(form)


class VirtualBoothUpdateForm(forms.ModelForm):
    class Meta:
        model = Sponsor
        fields = ('virtual_booth_content_ko', 'virtual_booth_content_en',)
        labels = {
            'virtual_booth_content': _('Virtual booth content')
        }
        widgets = {
            'virtual_booth_content_ko': SummernoteInplaceWidget(),
            'virtual_booth_content_en': SummernoteInplaceWidget(),
        }

    def __init__(self, *args, **kwargs):
        super(VirtualBoothUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', _('Submit')))
