from django.shortcuts import render, reverse, redirect
from django.views.generic import ListView, DetailView, UpdateView
from django.views import View
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext as _
from django.urls import reverse
from .models import Sponsor, SponsorLevel
from .forms import SponsorForm, VirtualBoothUpdateForm
import constance
import datetime
KST = datetime.timezone(datetime.timedelta(hours=9))


class SponsorList(ListView):
    model = Sponsor


class SponsorDetail(DetailView):
    model = Sponsor


class SponsorProposal(View):
    def get(self, request):
        has_submitted_sponsor = Sponsor.objects.filter(creator=request.user).exists()

        if has_submitted_sponsor is True:
            sponsor_obj = Sponsor.objects.get(creator=request.user)
            return redirect('sponsor_detail', sponsor_obj.slug)
        else:
            return redirect('sponsor_propose')


class SponsorUpdate(SuccessMessageMixin, UpdateView):
    form_class = SponsorForm
    template_name = "sponsor/sponsor_form.html"
    success_message = _(
        "후원사 신청이 성공적으로 처리되었습니다. 준비위원회 리뷰 이후 안내 메일을 발송드리도록 하겠습니다.")

    def get_object(self, queryset=None):
        sponsor, _ = Sponsor.objects.get_or_create(creator=self.request.user)
        self.SLUG = sponsor.slug

        return sponsor

    def get(self, request, *args, **kwargs):
        opening = constance.config.CFS_OPEN.astimezone(KST)
        deadline = constance.config.CFS_DEADLINE.astimezone(KST)
        now = datetime.datetime.now(tz=KST)
        has_accepted_sponsor = Sponsor.objects.filter(
            creator=request.user, accepted=True).exists()
        form = self.form_class(initial=self.initial)
        if has_accepted_sponsor:
            return render(request, self.template_name, {'form': form})
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
        return super(SponsorUpdate, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('sponsor', kwargs={'slug': self.SLUG})


class VirtualBooth(ListView):
    queryset = Sponsor.objects.filter(accepted=True)
    template_name = "sponsor/virtual_booth_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keystone = SponsorLevel.objects.filter(slug='keystone')
        diamond = SponsorLevel.objects.filter(slug='diamond')
        start_up = SponsorLevel.objects.filter(slug='start_up')
        try:
            context['keystone'] = keystone[0]
            context['diamond'] = diamond[0]
            context['start_up'] = start_up[0]
        except IndexError:
            pass
        context['title'] = "Virtual Booth"
        return context


class VirtualBoothDetail(DetailView):
    model = Sponsor
    template_name = "sponsor/virtual_booth_detail.html"

    def get_context_data(self, **kwargs):
        context = super(VirtualBoothDetail, self).get_context_data(**kwargs)

        return context


class VirtualBoothUpdate(UpdateView):
    form_class = VirtualBoothUpdateForm
    model = Sponsor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Virtual booth 내용 수정하기')
        context['content'] = Sponsor.objects.filter(creator=self.request.user, accepted=True, paid_at=None)
        return context

    def get_success_url(self):
        slug = Sponsor.objects.get(creator=self.request.user, accepted=True, paid_at__isnull=False).slug

        return reverse('virtual_booth', kwargs={'slug': slug})
