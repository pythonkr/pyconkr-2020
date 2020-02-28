from django import forms
from django_summernote.widgets import SummernoteInplaceWidget
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.files.images import get_image_dimensions
from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper
from .models import Profile


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['name_ko'].required = True
        self.fields['name_en'].required = True
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
        fields = ('name_ko', 'name_en', 'phone', 'email',
                  'organization', 'image', 'bio_ko', 'bio_en')
        widgets = {
            'bio': SummernoteInplaceWidget(),
        }
        labels = {
            'image': _('Photo'),
        }

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
