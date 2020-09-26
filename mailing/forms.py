from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import NewsLetter


class NewsLetterAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewsLetterAddForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', _('Submit')))

    class Meta:
        model = NewsLetter
        fields = ('email_address',)
        labels = {
            'email_address': _('이메일 주소')
        }


class SlackAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SlackAddForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', _('Submit')))
        self.fields['agree_coc'].required = True

    class Meta:
        model = NewsLetter
        fields = ('email_address', 'agree_coc')
        labels = {
            'email_address': _('이메일 주소'),
            'agree_coc': _('CoC 동의 (필수)'),
        }
