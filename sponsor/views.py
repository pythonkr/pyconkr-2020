from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext as _
from django.urls import reverse
from .models import Sponsor, SponsorLevel
from .forms import SponsorForm, VirtualBoothUpdateForm
import constance
import datetime
from program import slack

KST = datetime.timezone(datetime.timedelta(hours=9))


class SponsorDetail(DetailView):
    model = Sponsor


class SponsorDetail(DetailView):
    model = Sponsor


class SponsorProposalDetail(DetailView):
    template_name = 'sponsor/sponsor_proposal_detail.html'

    def get(self, request, *args, **kwargs):
        has_submitted_cfs = Sponsor.objects.filter(creator=request.user).exists()
        if not has_submitted_cfs:
            return redirect('sponsor_propose')

        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(Sponsor, creator=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SponsorCreate(SuccessMessageMixin, CreateView):
    model = Sponsor
    form_class = SponsorForm
    template_name = "sponsor/sponsor_form.html"
    success_message = _(
        "후원사 신청이 성공적으로 처리되었습니다. 준비위원회 리뷰 이후 안내 메일을 발송드리도록 하겠습니다.")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.save()
        return super(SponsorCreate, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        has_submitted_cfs = Sponsor.objects.filter(creator=request.user).exists()

        if has_submitted_cfs is True:
            return redirect('sponsor_proposal_detail')

        opening = constance.config.CFS_OPEN.astimezone(KST)
        deadline = constance.config.CFS_DEADLINE.astimezone(KST)
        now = datetime.datetime.now(tz=KST)

        if now < opening:
            return render(request, 'simple.html', {
                'title': _('후원사 모집이 아직 시작되지 않았습니다.🤖'),
                'content': _('모집 기간은 {} ~ {} 이니 일정에 참고해주세요.').format(
                    opening.strftime("%Y-%m-%d %H:%M"), deadline.strftime("%Y-%m-%d %H:%M"))})
        if now > deadline:
            return render(request, 'simple.html', {
                'title': _('후원사 모집이 종료되었습니다.🤖'),
                'content': _('모집 기간은 {} ~ {} 였습니다. 내년에 다시 개최될 파이콘 한국을 기대해주세요').format(
                    opening.strftime("%Y-%m-%d %H:%M"), deadline.strftime("%Y-%m-%d %H:%M"))})
        return super(SponsorCreate, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('sponsor_proposal_detail')


class SponsorUpdate(SuccessMessageMixin, UpdateView):
    form_class = SponsorForm
    template_name = "sponsor/sponsor_form.html"
    success_message = _(
        "후원사 신청이 성공적으로 처리되었습니다. 준비위원회 리뷰 이후 안내 메일을 발송드리도록 하겠습니다.")

    def get(self, request, *args, **kwargs):
        has_submitted_cfs = Sponsor.objects.filter(creator=request.user).exists()
        if not has_submitted_cfs:
            return redirect('sponsor_propose')

        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        sponsor = Sponsor.objects.get(creator=self.request.user)

        return sponsor

    def get_success_url(self):
        # slack.new_cfs_registered(self.request.META['HTTP_ORIGIN'], self.object.id, self.object.title)
        return reverse('sponsor_proposal_detail')


class VirtualBooth(ListView):
    queryset = Sponsor.objects.filter(accepted=True, paid_at__isnull=False)
    template_name = "sponsor/virtual_booth_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keystone = SponsorLevel.objects.filter(slug='keystone')
        diamond = SponsorLevel.objects.filter(slug='diamond')
        sapphire = SponsorLevel.objects.filter(slug='sapphire')
        start_up = SponsorLevel.objects.filter(slug='start_up')
        try:
            context['keystone'] = keystone[0]
            context['diamond'] = diamond[0]
            context['sapphire'] = sapphire[0]
            context['start_up'] = start_up[0]
        except IndexError:
            pass
        context['title'] = "Virtual Booth"
        return context


class VirtualBoothDetail(DetailView):
    model = Sponsor
    template_name = "sponsor/virtual_booth_detail.html"

    def get(self, request, *args, **kwargs):
        level = Sponsor.objects.get(slug=self.kwargs['slug']).level
        has_virtual_booth = SponsorLevel.objects.get(name=level).order < 5
        if not has_virtual_booth:
            return redirect('virtual_booth_home')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(VirtualBoothDetail, self).get_context_data(**kwargs)
        is_editable = Sponsor.objects.filter(
            creator=self.request.user, accepted=True, paid_at__isnull=False).exists()
        context['EDITABLE'] = is_editable

        return context


class VirtualBoothUpdate(UpdateView):
    form_class = VirtualBoothUpdateForm
    model = Sponsor
    template_name = "sponsor/virtual_booth_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        slug = Sponsor.objects.get(creator=self.request.user, accepted=True, paid_at__isnull=False).slug

        return reverse('virtual_booth', kwargs={'slug': slug})
