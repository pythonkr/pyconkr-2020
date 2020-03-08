from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext as _
from .models import Sponsor
from .forms import SponsorForm


class SponsorList(ListView):
    model = Sponsor


class SponsorDetail(DetailView):
    model = Sponsor


class SponsorCreate(SuccessMessageMixin, CreateView):
    form_class = SponsorForm
    template_name = "sponsor/sponsor_form.html"
    success_message = _(
        "후원사 신청이 성공적으로 처리되었습니다. 준비위원회 리뷰 이후 안내 메일을 발송드리도록 하겠습니다.")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.save()
        return super(SponsorCreate, self).form_valid(form)

    # def dispatch(self, request, *args, **kwargs):
    #     if Proposal.objects.filter(user=request.user).exists():
    #         return redirect('proposal')
    #     if request.user.profile.name == '':
    #         return redirect('profile_edit')
    #     return super(ProposalCreate, self).dispatch(request, *args, **kwargs)

    # def get_success_url(self):
    #     return reverse('proposal')
