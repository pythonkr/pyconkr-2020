from crispy_forms.layout import Submit
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, CreateView, View
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.utils.translation import ugettext as _
from django.urls import reverse

import re
from .models import Sponsor, SponsorLevel
from .forms import SponsorForm, VirtualBoothUpdateForm
from pyconkr.views import get_KST_now
import constance
from program import slack


class SponsorDetail(DetailView):
    model = Sponsor

    def get_context_data(self, **kwargs):
        context = super(SponsorDetail, self).get_context_data(**kwargs)
        user = self.request.user
        is_editable = user.is_authenticated and (
                Sponsor.objects.filter(creator=user, accepted=True, paid_at__isnull=False,
                                       slug=self.kwargs['slug']).exists()
                or Sponsor.objects.filter(manager_id=user, accepted=True,
                                          paid_at__isnull=False,
                                          slug=self.kwargs['slug']).exists())
        context['EDITABLE'] = is_editable
        return context


class SponsorProposalHome(ListView):
    model = SponsorLevel
    template_name = 'sponsor/sponsor_proposal_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        level_remain = dict()
        for level in SponsorLevel.objects.filter(order__lte=4):
            if level.order == 0:  # 준비위를 위한 빈 자리
                continue
            if level.limit - Sponsor.objects.filter(level=level, accepted=True).__len__() <= 0:
                level_remain[level.name] = _("마감")
            else:
                level_remain[level.name] = "{remain}/{limit}".format(remain=level.limit - Sponsor.objects.filter(
                    level=level, accepted=True).__len__(), limit=level.limit)
        context['remains'] = level_remain

        KST, now = get_KST_now()
        context['CFS_start_at'] = constance.config.CFS_OPEN.replace(tzinfo=KST)
        context['CFS_finish_at'] = constance.config.CFS_CLOSE.replace(tzinfo=KST)

        return context


class SponsorProposalDetail(DetailView):
    template_name = 'sponsor/sponsor_proposal_detail.html'

    def get(self, request, *args, **kwargs):
        if Sponsor.objects.filter(creator=self.request.user).exists():
            written_cfs = Sponsor.objects.filter(creator=self.request.user)
        elif Sponsor.objects.filter(manager_id=self.request.user).exists():
            written_cfs = Sponsor.objects.filter(manager_id=self.request.user)
        else:
            return redirect('sponsor_propose')

        # 제출 상태로 변경 처리
        if request.GET.get('submit') == '1':
            cfs_obj = written_cfs.get()
            cfs_obj.submitted = True
            cfs_obj.save()
            # GET params 생략을 위한 redirect 처리
            return redirect('sponsor_proposal_detail')

        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if Sponsor.objects.filter(creator=self.request.user).exists():
            return get_object_or_404(Sponsor, creator=self.request.user)
        elif Sponsor.objects.filter(manager_id=self.request.user).exists():
            return get_object_or_404(Sponsor, manager_id=self.request.user)

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
        has_submitted_cfs = Sponsor.objects.filter(
            creator=request.user).exists() or Sponsor.objects.filter(manager_id=request.user).exists()

        if has_submitted_cfs is True:
            return redirect('sponsor_proposal_detail')

        KST, now = get_KST_now()
        opening = constance.config.CFS_OPEN.astimezone(KST)
        deadline = constance.config.CFS_CLOSE.astimezone(KST)

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

        form.helper.add_input(
            Submit('save', _('Save'), formaction=save_btn_url))
        form.helper.add_input(
            Submit('submit', _('Submit'), formaction=submit_btn_url))

        return form

    def get_success_url(self):
        if self.object.submitted is True:
            slack.new_cfs_registered(
                self.request.META['HTTP_ORIGIN'], self.object.id, self.object.name)
        return reverse('sponsor_proposal_detail')


class SponsorUpdate(SuccessMessageMixin, UpdateView):
    form_class = SponsorForm
    template_name = "sponsor/sponsor_form.html"
    success_message = _(
        "후원사 신청이 성공적으로 처리되었습니다. 준비위원회 리뷰 이후 안내 메일을 발송드리도록 하겠습니다.")

    def get(self, request, *args, **kwargs):
        has_submitted_cfs = Sponsor.objects.filter(
            creator=request.user).exists() or Sponsor.objects.filter(manager_id=request.user).exists()
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
        save_btn_url = reverse('sponsor_proposal_edit') + \
                       '?go_proposal={}&submit=0'.format(self.go_proposal)
        form.helper.add_input(
            Submit('save', _('Save'), formaction=save_btn_url))

        if self.object.submitted is False:
            submit_btn_url = reverse(
                'sponsor_proposal_edit') + '?&go_proposal={}&submit=1'.format(self.go_proposal)
            form.helper.add_input(
                Submit('submit', _('Submit'), formaction=submit_btn_url))

        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['go_proposal'] = self.go_proposal
        return context

    def get_object(self, queryset=None):
        if Sponsor.objects.filter(creator=self.request.user).exists():
            return Sponsor.objects.get(creator=self.request.user)
        elif Sponsor.objects.filter(manager_id=self.request.user).exists():
            return Sponsor.objects.get(manager_id=self.request.user)

    def get_success_url(self):
        if self.go_proposal == '1':
            return reverse('sponsor_proposal_detail')
        else:
            return reverse('sponsor_detail', kwargs={'slug': self.object.slug})


def summernoteFilter(code):
    filter_list = [
        # s3 request issue
        [r'(?<=amazonaws\.com/django-summernote/\d{4}-\d{2}-\d{2}/[\w\-]{36}\.\w{3})\?.*?(?=")', ''],
        [r'(?<=amazonaws\.com/django-summernote/\d{4}-\d{2}-\d{2}/[\w\-]{36}\.\w{4})\?.*?(?=")', ''],

        # no effect style
        [r'\s?letter-spacing: -0.32px;?\s?', ''],
        [r'</?o:p>', ''],

        # empty attr
        [r'\s?style=""', ''],

        # empty tag
        [r'<p></p>\n?', ''],
        [r'<p\s[^>]*?></p>', ''],
        [r'<span\s[^>]*?></span>', ''],
    ]
    html_code = code
    for f in filter_list:
        html_code = re.sub(f[0], f[1], html_code)

    return html_code


def is_sponsor_manager(user):
    managers = []
    for sponsor in Sponsor.objects.filter(accepted=True, paid_at__isnull=False):
        managers.append(sponsor.creator)
        managers.append(sponsor.manager_id)
    for super_user in User.objects.filter(is_staff=True):
        managers.append(super_user)

    return user in managers


class VirtualBooth(ListView):
    queryset = Sponsor.objects.filter(accepted=True, paid_at__isnull=False)
    template_name = "sponsor/virtual_booth_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Virtual Booth"
        context['is_empty'] = not Sponsor.objects.filter(
            accepted=True, paid_at__isnull=False, logo_image__isnull=False).exists()
        context['booths'] = Sponsor.objects \
            .filter(level__order__lt=5, accepted=True, paid_at__isnull=False, logo_image__isnull=False) \
            .exclude(level__order=0).order_by('level__order', 'paid_at')
        try:
            context['sample'] = Sponsor.objects.get(level__order=0)
        except Sponsor.DoesNotExist:
            pass

        KST, now = get_KST_now()
        context['is_manager'] = is_sponsor_manager(self.request.user)
        context['is_opened'] = constance.config.VIRTUAL_BOOTH_OPEN <= now

        return context


class VirtualBoothDetail(DetailView):
    model = Sponsor
    template_name = "sponsor/virtual_booth_detail.html"

    def get(self, request, *args, **kwargs):
        KST, now = get_KST_now()
        is_visible = is_sponsor_manager(self.request.user) or constance.config.VIRTUAL_BOOTH_OPEN <= now
        if not is_visible:
            return redirect('virtual_booth_home')

        level = Sponsor.objects.get(slug=self.kwargs['slug']).level
        has_virtual_booth = SponsorLevel.objects.get(name=level).order < 5
        if not has_virtual_booth:
            return redirect('virtual_booth_home')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(VirtualBoothDetail, self).get_context_data(**kwargs)
        user = self.request.user
        KST, now = get_KST_now()

        is_editable = constance.config.VIRTUAL_BOOTH_EDITABLE and user.is_authenticated and (
                Sponsor.objects.filter(creator=user, accepted=True, paid_at__isnull=False,
                                       slug=self.kwargs['slug']).exists()
                or Sponsor.objects.filter(manager_id=user, accepted=True, paid_at__isnull=False,
                                          slug=self.kwargs['slug']).exists()) and (
                              now < constance.config.VIRTUAL_BOOTH_EDIT_FINISH or now > constance.config.VIRTUAL_BOOTH_OPEN)
        context['is_editable'] = is_editable

        return context


class VirtualBoothUpdate(UpdateView):
    form_class = VirtualBoothUpdateForm
    model = Sponsor
    template_name = "sponsor/virtual_booth_update.html"

    def get(self, request, *args, **kwargs):
        KST, now = get_KST_now()
        is_editable = constance.config.VIRTUAL_BOOTH_EDITABLE and self.request.user.is_authenticated and (
                Sponsor.objects.filter(creator=self.request.user, accepted=True, paid_at__isnull=False,
                                       slug=self.kwargs['slug']).exists()
                or Sponsor.objects.filter(manager_id=self.request.user, accepted=True, paid_at__isnull=False,
                                          slug=self.kwargs['slug']).exists()) and (
                              now < constance.config.VIRTUAL_BOOTH_EDIT_FINISH or now > constance.config.VIRTUAL_BOOTH_OPEN)
        if not is_editable:
            return redirect('virtual_booth_home')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            form.instance.virtual_booth_content_ko = summernoteFilter(form.instance.virtual_booth_content_ko)
            form.instance.virtual_booth_content_en = summernoteFilter(form.instance.virtual_booth_content_en)
        except TypeError:
            pass
        form.save()

        return super(VirtualBoothUpdate, self).form_valid(form)

    def get_success_url(self):
        KST, now = get_KST_now()
        if now > constance.config.VIRTUAL_BOOTH_OPEN:
            slack.virtual_booth_updated(self.request.META['HTTP_ORIGIN'], self.object.slug, self.object.name)
        return reverse('virtual_booth', kwargs={'slug': self.object.slug})


class LoginForSponsor(View):
    template_name = 'sponsor/sponsor_login_form.html'

    def get(self, request):
        context = dict()
        context['error'] = request.session.get('retry', False)
        return render(request, self.template_name, context)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            # 로그인 성공 시 이전에 실패한 이력 삭제
            try:
                del request.session['retry']
            except KeyError:
                # 실패 이력 없음
                pass

            login(request, user)
            return redirect('index')
        else:
            # 로그인 실패
            request.session['retry'] = True
            return redirect('login_for_sponsor')
