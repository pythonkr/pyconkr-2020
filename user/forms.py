# from allauth.account.forms import BaseSignupForm
from contextlib import suppress
import random
import string
from PIL import Image
from io import BytesIO
from django.core.files import File
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
        self.fields['image_ori'].help_text += _('Maximum size is %(size)d MB') \
            % {'size': settings.SPEAKER_IMAGE_MAXIMUM_FILESIZE_IN_MB}
        self.fields['image_ori'].help_text += ' / ' \
            + _('Minimum dimension is %(width)d x %(height)d') \
            % {'width': settings.SPEAKER_IMAGE_MINIMUM_DIMENSION[0],
               'height': settings.SPEAKER_IMAGE_MINIMUM_DIMENSION[1]}

    class Meta:
        model = Profile
        fields = ('name_ko', 'name_en', 'email', 'phone',
                  'organization', 'image_ori', 'bio_ko', 'bio_en', 'agreement_receive_advertising_info')
        widgets = {
            'bio': SummernoteInplaceWidget(),
        }
        labels = {
            'name_ko': _('이름 (한글)'),
            'name_en': _('이름 (영어)'),
            'image_ori': _('Photo'),
            'agreement_receive_advertising_info': _('홍보성 메일 수신 동의')
        }

    def save(self, commit=True):
        # Update user email
        user = self.instance.user
        email = self.cleaned_data['email']
        if email != user.email:
            user.email = self.cleaned_data['email']
            user.save()

        # Make user code
        profile = self.instance
        if not profile.user_code:
            length = 20
            pool = string.ascii_letters + string.digits

            while True:
                result = ""
                for _ in range(length):
                    result += random.choice(pool)

                if not Profile.objects.filter(user_code=result).exists():
                    break

            profile.user_code = result
            profile.save()

        # Optimize user profile image
        image = self.instance.image_ori
        small_image_size = 256
        new_width = 0
        new_height = 0
        if image.width >= image.height:
            new_height = small_image_size
            new_width = int(small_image_size * image.width / image.height)
        else:
            new_width = small_image_size
            new_height = int(small_image_size * image.height / image.width)

        try:
            PIL_image = Image.open(image.file)
            image_small = PIL_image.resize((new_width, new_height))
            blob = BytesIO()
            image_small.save(blob, 'PNG')
            self.instance.image_small.save(image.name+'_small.jpg', File(blob), save=False)
            self.instance.save()
        except ValueError:  # 동일한 파일 입력
            pass

        return super(ProfileForm, self).save(commit=commit)

    def clean_image(self):
        image = self.cleaned_data.get('image_ori')
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
