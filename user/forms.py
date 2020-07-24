# from allauth.account.forms import BaseSignupForm
from contextlib import suppress
from django.urls.exceptions import NoReverseMatch
from crispy_forms.bootstrap import InlineCheckboxes
from allauth.socialaccount.forms import SignupForm
from django import forms
from django_summernote.widgets import SummernoteInplaceWidget
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.files.images import get_image_dimensions
from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper
from .models import Profile
from django.urls import reverse
from django.db import transaction
from django.contrib.auth import get_user_model
UserModel = get_user_model()


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['name_ko'].required = True
        self.fields['name_en'].required = True
        self.fields['email'].initial = self.instance.user.email
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', _('Submit')))
        self.fields['image'].help_text += _('Maximum size is %(size)d MB') \
            % {'size': settings.SPEAKER_IMAGE_MAXIMUM_FILESIZE_IN_MB}
        self.fields['image'].help_text += ' / ' \
            + _('Minimum dimension is %(width)d x %(height)d') \
            % {'width': settings.SPEAKER_IMAGE_MINIMUM_DIMENSION[0],
               'height': settings.SPEAKER_IMAGE_MINIMUM_DIMENSION[1]}

    class Meta:
        model = Profile
        fields = ('name_ko', 'name_en', 'email', 'phone',
                  'organization', 'image', 'bio_ko', 'bio_en', 'agreement_receive_advertising_info')
        widgets = {
            'bio': SummernoteInplaceWidget(),
        }
        labels = {
            'image': _('Photo'),
        }

    def save(self, commit=True):
        user = self.instance.user
        email = self.cleaned_data['email']
        if email != user.email:
            user.email = self.cleaned_data['email']
            user.save()
        return super(ProfileForm, self).save(commit=commit)

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            try:
                if image._size > settings.SPEAKER_IMAGE_MAXIMUM_FILESIZE_IN_MB * 1024 * 1024:
                    raise forms.ValidationError(
                        _('Maximum size is %(size)d MB')
                        % {'size': settings.SPEAKER_IMAGE_MAXIMUM_FILESIZE_IN_MB}
                    )
            except AttributeError:
                pass

            w, h = get_image_dimensions(image)
            if w < settings.SPEAKER_IMAGE_MINIMUM_DIMENSION[0] \
                    or h < settings.SPEAKER_IMAGE_MINIMUM_DIMENSION[1]:
                raise forms.ValidationError(
                    _('Minimum dimension is %(width)d x %(height)d')
                    % {'width': settings.SPEAKER_IMAGE_MINIMUM_DIMENSION[0],
                       'height': settings.SPEAKER_IMAGE_MINIMUM_DIMENSION[1]}
                )

        return image


class SocialSignupForm(SignupForm):
    email = forms.EmailField(label=_('이메일'), help_text=_(
        '파이콘 행사에 관련된 안내 메일을 받을 이메일 주소를 입력해주세요.'))
    name = forms.CharField(max_length=100, label=_(
        '이름'), help_text=_('기입한 이름이 행사 당일 이름표에 표시됩니다.'))
    organization = forms.CharField(max_length=100, required=False, label=_(
        '소속'), help_text=_('기입한 조직명이 행사 당일 이름표에 표시됩니다. 필수 입력 사항은 아닙니다.'))

    checked_terms_of_service = forms.BooleanField()
    checked_privacy_policy = forms.BooleanField()
    checked_coc = forms.BooleanField()

    def __init__(self, *args, **kwargs):
        super(SocialSignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].initial = self.sociallogin.user.email
        self.fields['username'].widget = forms.HiddenInput()
        self.set_form()
        self.set_agreement_labels()

    def set_agreement_labels(self):
        terms_of_service_text = _("이용 약관에 동의합니다.")
        self.fields['checked_terms_of_service'].label = f'''
        <a target="_blank" {self.reserve_flatpage_with_href_attr('2020/terms-of-service/')}">
          {terms_of_service_text}
        </a>
        '''
        checked_privacy_text = _("개인정보 처리방침에 동의합니다.")
        self.fields['checked_privacy_policy'].label = f'''
        <a target="_blank" {self.reserve_flatpage_with_href_attr('2020/privacy-policy/')}">
          {checked_privacy_text}
        </a>
        '''
        coc_text = _("파이콘 한국 행동 강령에 동의합니다.")
        self.fields['checked_coc'].label = f'''
        <a target="_blank" {self.reserve_flatpage_with_href_attr('2020/about/coc/')}">
          {coc_text}
        </a>
        '''

    def reserve_flatpage_with_href_attr(self, url):
        try:
            reserved_url = reverse('flatpage', kwargs={'url': url})
            return f'href="{reserved_url}"'
        except NoReverseMatch as e:
            pass
        return ''

    def set_form(self):
        self.helper = FormHelper()
        self.helper.form_id = 'signup_form'
        self.helper.form_class = 'signup'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('socialaccount_signup')
        self.helper.add_input(Submit('submit', _('가입하기')))

    @transaction.atomic
    def save(self, request, commit=True):
        user = super(SocialSignupForm, self).save(request)
        user.email = self.cleaned_data['email']
        user.save()
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.name = self.cleaned_data['name']
        profile.organization = self.cleaned_data['organization']
        profile.save()
        return user
