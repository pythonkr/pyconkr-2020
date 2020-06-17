from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext as _
from .models import Sponsor
from .forms import SponsorForm
import constance
import datetime
KST = datetime.timezone(datetime.timedelta(hours=9))


class SponsorList(ListView):
    model = Sponsor


class SponsorDetail(DetailView):
    model = Sponsor


class SponsorUpdate(SuccessMessageMixin, UpdateView):
    form_class = SponsorForm
    template_name = "sponsor/sponsor_form.html"
    success_message = _(
        "후원사 신청이 성공적으로 처리되었습니다. 준비위원회 리뷰 이후 안내 메일을 발송드리도록 하겠습니다.")

    def get_object(self, queryset=None):
        sponsor, _ = Sponsor.objects.get_or_create(creator=self.request.user)
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


class VirtualBooth(DetailView):
    template_name = "sponsor/virtual_booth_home.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'title': _('Virtual Booth')
        })
