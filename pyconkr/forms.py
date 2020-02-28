# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.urls import reverse


class EmailLoginForm(forms.Form):
    email = forms.EmailField(
        max_length=255,
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Email address',
            'class': 'form-control',
        })
    )

    def __init__(self, *args, **kwargs):
        super(EmailLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', _('Login')))

    def clean(self):
        cleaned_data = super(EmailLoginForm, self).clean()
        return cleaned_data
