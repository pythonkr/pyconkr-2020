from django import forms
from django_summernote.widgets import SummernoteInplaceWidget
from django.utils.translation import ugettext as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Sponsor, SponsorLevel

from django.forms import ModelChoiceField


class SponsorLevelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
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
        self.helper.add_input(Submit('save', _('Save')))
        self.helper.add_input(Submit('submit', _('Submit')))

        self.fields['name_ko'].required = True
        self.fields['name_ko'].required = True
        self.fields['level'] = SponsorLevelChoiceField(
            queryset=SponsorLevel.objects.filter(visible=True))

    def form_valid(self, form):
        if self.request.POST['submit'] == 'save':
            return super(SongEditView, self).form_valid(form)


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
