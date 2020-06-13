from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django import forms
from django.conf import settings
from django_summernote.widgets import SummernoteInplaceWidget
from django.utils.translation import ugettext_lazy as _
from django.core.files.images import get_image_dimensions
from .models import Speaker, Program, Proposal, SprintProposal, TutorialProposal, ProgramCategory

from constance import config


class SpeakerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SpeakerForm, self).__init__(*args, **kwargs)
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
        model = Speaker
        fields = ('image', 'desc', 'info', )
        widgets = {
            'desc': SummernoteInplaceWidget(),
        }
        labels = {
            'image': _('Photo'),
            'desc': _('Profile'),
            'info': _('Additional information'),
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


class ProgramForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProgramForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', _('Submit')))

    class Meta:
        model = Program
        fields = ('name', 'slide_url', 'video_url', 'is_recordable', 'desc', )
        widgets = {
            'desc': SummernoteInplaceWidget(),
        }
        labels = {
            'name': _('Title'),
            'slide_url': _('Slide URL'),
            'video_url': _('Video URL'),
            'is_recordable': _('Photography and recording is allowed.'),
            'desc': _('Description'),
        }


class ProposalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProposalForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', _('Submit')))

        self.fields['brief'].initial = config.CFP_BRIEF_TEMPLATE
        self.fields['desc'].initial = config.CFP_DESC_TEMPLATE

    class Meta:
        model = Proposal
        fields = ('title', 'brief', 'desc', 'comment',
                  'difficulty', 'duration', 'language',)
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
            'language': _('Language'),
        }


class SprintProposalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SprintProposalForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', _('Submit')))

    class Meta:
        model = SprintProposal
        fields = ('title', 'language', 'project_url',
                  'project_brief', 'contribution_desc',)
        widgets = {
            'contribution_desc': SummernoteInplaceWidget(),
            'comment': SummernoteInplaceWidget(),
        }

        labels = {
            'title': _('Title'),
            'language': _('Language'),
            'project_url': _('Project URL'),
            'project_brief': _('Project brief'),
            'contribution_desc': _('Contribution description')
        }


class TutorialProposalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TutorialProposalForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', _('Submit')))

    class Meta:
        model = TutorialProposal
        fields = ('title', 'brief', 'desc', 'difficulty', )
        widgets = {
            'desc': SummernoteInplaceWidget(),
            'comment': SummernoteInplaceWidget(),
        }

        labels = {
            'title': _('Title'),
            'brief': _('Brief'),
            'desc': _('Detailed description'),

            'difficulty': _('Session difficulty'),
        }
