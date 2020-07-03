from crispy_forms.layout import Submit, Button
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
from django.contrib.auth.models import User

KST = datetime.timezone(datetime.timedelta(hours=9))


class SponsorDetail(DetailView):
    model = Sponsor

    def get_context_data(self, **kwargs):
        context = super(SponsorDetail, self).get_context_data(**kwargs)
        is_editable = Sponsor.objects.filter(
            creator=self.request.user, accepted=True, paid_at__isnull=False, slug=self.kwargs['slug']).exists()
        context['EDITABLE'] = is_editable

        return context


class SponsorProposalHome(ListView):
    model = SponsorLevel
    template_name = 'sponsor/sponsor_proposal_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        level_remain = dict()
        for level in SponsorLevel.objects.filter(order__lte=4):
            if level.limit - Sponsor.objects.filter(level=level, accepted=True).__len__() <= 0:
                level_remain[level.name] = _("마감")
            else:
                level_remain[level.name] = "{remain}/{limit}".format(remain=level.limit - Sponsor.objects.filter(level=level, accepted=True).__len__(), limit=level.limit)
        context['remains'] = level_remain

        KST = datetime.timezone(datetime.timedelta(hours=9))
        context['CFS_start_at'] = constance.config.CFS_OPEN.replace(tzinfo=KST)
        context['CFS_finish_at'] = constance.config.CFS_DEADLINE.replace(tzinfo=KST)

        return context


class SponsorProposalDetail(DetailView):
    template_name = 'sponsor/sponsor_proposal_detail.html'

    def get(self, request, *args, **kwargs):
        written_cfs = Sponsor.objects.filter(creator=self.request.user)
        if not written_cfs.exists():
            return redirect('sponsor_propose')

        # 제출상태로 변경처리
        if request.GET.get('submit') == '1':
            cfs_obj = written_cfs.get()
            cfs_obj.submitted = True
            cfs_obj.save()
            return redirect('sponsor_proposal_detail')  # GET params 생략을 위한 redirect 처리

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
        form.instance.submitted = self.is_submitted
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

    def post(self, request, *args, **kwargs):
        # submit get Parameter 기본값 설정
        if request.GET.get('submit') is None or request.GET['submit'] == '0':
            self.is_submitted = False
        elif request.GET['submit'] == '1':
            self.is_submitted = True

        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        save_btn_url = reverse('sponsor_propose') + '?submit=0'
        submit_btn_url = reverse('sponsor_propose') + '?submit=1'

        form.helper.add_input(Submit('save', _('Save'), formaction=save_btn_url))
        form.helper.add_input(Submit('submit', _('Submit'), formaction=submit_btn_url))

        return form

    def get_success_url(self):
        if self.object.submitted is True:
            slack.new_cfs_registered(self.request.META['HTTP_ORIGIN'], self.object.id, self.object.name)
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

        # sponsor_detail 페이지에서 온 경우 go_proposal=0
        # sponsor_proposal_detail에서 온 경우 go_proposal=1
        self.go_proposal = request.GET['go_proposal']

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        if self.is_submitted is True:
            form.instance.submitted = True
        form.save()
        return super(SponsorUpdate, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.go_proposal = request.GET['go_proposal']

        # submit get Parameter 기본값 설정
        if request.GET.get('submit') is None or request.GET['submit'] == '0':
            self.is_submitted = False
        elif request.GET['submit'] == '1':
            self.is_submitted = True

        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        save_btn_url = reverse('sponsor_proposal_edit') + '?go_proposal={}&submit=0'.format(self.go_proposal)
        form.helper.add_input(Submit('save', _('Save'), formaction=save_btn_url))

        if self.object.submitted is False:
            submit_btn_url = reverse('sponsor_proposal_edit') + '?&go_proposal={}&submit=1'.format(self.go_proposal)
            form.helper.add_input(Submit('submit', _('Submit'), formaction=submit_btn_url))

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['go_proposal'] = self.go_proposal
        return context

    def get_object(self, queryset=None):
        sponsor = Sponsor.objects.get(creator=self.request.user)
        return sponsor

    def get_success_url(self):
        # slack.cfs_updated(self.request.META['HTTP_ORIGIN'], self.object.id, self.object.name)
        if self.go_proposal == '1':
            return reverse('sponsor_proposal_detail')
        else:
            return reverse('sponsor_detail', kwargs={'slug': self.object.slug})


class VirtualBooth(ListView):
    queryset = Sponsor.objects.filter(accepted=True, paid_at__isnull=False)
    template_name = "sponsor/virtual_booth_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Virtual Booth"
        context['is_empty'] = not Sponsor.objects.filter(accepted=True, paid_at__isnull=False).exists()

        managers = []
        for sponsor in Sponsor.objects.filter(accepted=True, paid_at__isnull=False):
            managers.append(sponsor.creator)
        for super_user in User.objects.filter(is_staff=True):
            managers.append(super_user)

        context['is_manager'] = self.request.user in managers

        now = datetime.date.today()
        virtual_booth_open_at = datetime.date(2020, 9, 21)
        context['is_opened'] = virtual_booth_open_at <= now

        return context


class VirtualBoothDetail(DetailView):
    model = Sponsor
    template_name = "sponsor/virtual_booth_detail.html"

    def get(self, request, *args, **kwargs):
        managers = []
        for sponsor in Sponsor.objects.filter(accepted=True, paid_at__isnull=False):
            managers.append(sponsor.creator)
        for super_user in User.objects.filter(is_staff=True):
            managers.append(super_user)

        is_visible = self.request.user in managers
        if not is_visible:
            return redirect('virtual_booth_home')

        level = Sponsor.objects.get(slug=self.kwargs['slug']).level
        has_virtual_booth = SponsorLevel.objects.get(name=level).order < 5
        if not has_virtual_booth:
            return redirect('virtual_booth_home')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(VirtualBoothDetail, self).get_context_data(**kwargs)
        is_editable = Sponsor.objects.filter(
            creator=self.request.user, accepted=True, paid_at__isnull=False, slug=self.kwargs['slug']).exists()
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
