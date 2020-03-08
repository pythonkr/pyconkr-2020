from django import forms
from django_summernote.widgets import SummernoteInplaceWidget
from django.utils.translation import ugettext as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Sponsor


class SponsorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SponsorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', _('Submit')))

    class Meta:
        model = Sponsor
        fields = ('level', 'logo_image', 'name_ko', 'name_en', 'url',
                  'desc_ko', 'desc_en', 'manager_name', 'manager_email',
                  'business_registration_number', 'business_registration_file',
                  'comment')
        widgets = {
            'desc_ko': SummernoteInplaceWidget(),
            'desc_en': SummernoteInplaceWidget(),
            'comment': SummernoteInplaceWidget(),
        }

        labels = {
            'level': _('후원사 등급'),
            'logo_image': _('로고 이미지'),
            'name_ko': _('후원사 이름(한글)'),
            'name_en': _('후원사 이름(영문)'),
            'url': _('후원사 홈페이지 주소'),
            'desc_ko': _('후원사 소개(한글)'),
            'desc_ko': _('후원사 소개(영문)'),
            'manager_name': _('후원 담당자 이름'),
            'manager_email': _('후원 담당자 이메일'),
            'business_registration_number': _('후원사 사업자 등록 번호'),
            'business_registration_file': _('후원사 사업자 등록증'),
            'comment': _('추가로 문의할 점'),
        }
