from django.views.generic import DetailView, UpdateView
from django.utils.translation import ugettext as _
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, get_object_or_404
from .models import Profile
from sponsor.models import Sponsor
from .forms import ProfileForm
from registration.models import Registration
from program.models import TutorialProposal, SprintProposal, Proposal
from program.models import TutorialCheckin, SprintCheckin


class ProfileDetail(DetailView):
    model = Profile

    def dispatch(self, request, *args, **kwargs):
        try:
            if not self.request.user.profile.name:
                return redirect('profile_edit')
        except Exception:
            return redirect('profile_edit')
        return super(ProfileDetail, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, pk=self.request.user.profile.pk)

    def get_context_data(self, **kwargs):
        context = super(ProfileDetail, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            if self.request.user == self.object.user:
                context['editable'] = True
        is_registered = Registration.objects.active_conference().filter(
            user=self.request.user,
            payment_status__in=['paid', 'ready']
        ).exists()
        context['sponsors'] = Sponsor.objects.filter(creator=self.request.user)
        context['proposals'] = Proposal.objects.filter(user=self.request.user)
        context['tickets'] = Registration.objects.filter(user=self.request.user, payment_status__in=['paid', 'ready'])
        context['joined_sprint'] = SprintCheckin.objects.filter(user=self.request.user)
        context['cancelled_tickets'] = Registration.objects.filter(user=self.request.user, payment_status='cancelled')
        context['is_registered'] = is_registered
        context['title'] = _("Profile")

        return context


class ProfileUpdate(SuccessMessageMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    success_message = _("Profile successfully updated.")

    def get_queryset(self):
        queryset = super(ProfileUpdate, self).get_queryset()
        return queryset.filter(user=self.request.user)

    def get_object(self, queryset=None):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return get_object_or_404(Profile, pk=profile.pk)

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdate, self).get_context_data(**kwargs)
        context['title'] = _("Update profile")
        return context
