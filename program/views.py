import random
import constance
import datetime
from pyconkr.views import get_KST_now
from functools import reduce

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext as _
from django.urls import reverse
from django.http import Http404
from django.views.generic.edit import ModelFormMixin

from crispy_forms.layout import Hidden

from .models import ProgramCategory, Proposal, OpenReview, LightningTalk, Sprint
from .forms import ProposalForm, OpenReviewCategoryForm, OpenReviewCommentForm, OpenReviewLanguageForm, \
    LightningTalkForm, ProgramUpdateForm
from .slack import new_cfp_registered, cfp_updated, program_updated


class ContributionHome(TemplateView):
    template_name = "pyconkr/contribution_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        KST, now = get_KST_now()
        context['cfp_open'] = constance.config.CFP_OPEN.replace(tzinfo=KST)
        context['cfp_close'] = constance.config.CFP_CLOSE.replace(tzinfo=KST)
        context['keynote_start_at'] = constance.config.KEYNOTE_RECOMMEND_OPEN.replace(tzinfo=KST)
        context['keynote_end_at'] = constance.config.KEYNOTE_RECOMMEND_CLOSE.replace(tzinfo=KST)
        context['review_start_at'] = constance.config.OPEN_REVIEW_START.replace(tzinfo=KST)
        context['review_finish_at'] = constance.config.OPEN_REVIEW_FINISH.replace(tzinfo=KST)
        context['lightning_talk_open'] = constance.config.LIGHTNING_TALK_OPEN.replace(tzinfo=KST)
        context['lightning_talk_close'] = constance.config.LIGHTNING_TALK_CLOSE.replace(tzinfo=KST)
        context['now'] = now
        return context


class ProgramList(ListView):
    queryset = ProgramCategory.objects.all().exclude(slug="opening").exclude(slug="closing")
    template_name = "pyconkr/program_list.html"
    ordering = ('id',)

    def get_context_data(self, **kwargs):
        context = super(ProgramList, self).get_context_data(**kwargs)
        context['programs'] = Proposal.objects.filter(accepted=True)
        context['accepted_exist'] = Proposal.objects.filter(accepted=True).exists()
        context['is_open'] = is_program_opened()
        categories = []
        for program in Proposal.objects.filter(accepted=True).exclude(category__slug="keynote"):
            categories.append(program.category)
        context['having_program'] = categories
        return context


class ProgramDetail(DetailView):
    model = Proposal
    template_name = "pyconkr/program_detail.html"

    def get(self, request, *args, **kwargs):
        if not is_program_opened() or not Proposal.objects.filter(pk=self.kwargs['pk'], accepted=True).exists():
            return redirect('talk-list')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProgramDetail, self).get_context_data(**kwargs)

        KST, now = get_KST_now()
        video_open_at = Proposal.objects.get(pk=self.kwargs['pk'], accepted=True).video_open_at
        if video_open_at:
            context['video_opened'] = now > video_open_at
        else:
            context['video_opened'] = False
        context['program'] = Proposal.objects.get(pk=self.kwargs['pk'], accepted=True)
        context['editable'] = constance.config.PROGRAM_DETAIL_EDITABLE \
                                and Proposal.objects.get(pk=self.kwargs['pk'], accepted=True).user == self.request.user
        return context


class ProgramUpdate(UpdateView):
    form_class = ProgramUpdateForm
    model = Proposal
    template_name = "pyconkr/program_update.html"

    def dispatch(self, request, *args, **kwargs):
        is_editable = constance.config.PROGRAM_DETAIL_EDITABLE and self.request.user.is_authenticated \
                      and Proposal.objects.filter(user=self.request.user, accepted=True).exists() \
                      and (str(Proposal.objects.get(user=self.request.user, accepted=True).pk) == self.kwargs['pk'])
        if not is_editable:
            return redirect('talk-list')

        return super(ProgramUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        program_updated(self.request.META['HTTP_ORIGIN'], self.object.id, self.object.title)
        return reverse('talk', kwargs={'pk': self.kwargs['pk']})


class ProgramSchedule(TemplateView):
    template_name = "schedule.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        KST, now = get_KST_now()
        context['is_open'] = now > constance.config.SCHEDULE_OPEN
        programs = Proposal.objects.filter(accepted=True, video_open_at__isnull=False, track_num__isnull=False)

        if not programs.exists():
            context['is_empty'] = True
            return context

        sat = list()
        sun = list()
        for p in programs:
            if (p.video_open_at + datetime.timedelta(hours=9)).replace(tzinfo=KST).weekday() == 5:
                sat.append({'program': p, 'time': p.video_open_at, 'track': p.track_num})
            elif (p.video_open_at + datetime.timedelta(hours=9)).replace(tzinfo=KST).weekday() == 6:
                sun.append({'program': p, 'time': p.video_open_at, 'track': p.track_num})

        def list_by_time(acc, cur):
            program = cur['program']
            time = cur['time']
            track = cur['track']
            if time not in acc.keys():
                acc[time] = ['', '', '']
                acc[time][track - 1] = program
            else:
                acc[time][track - 1] = program
            return acc

        sat_ = reduce(list_by_time, sat, {})
        sun_ = reduce(list_by_time, sun, {})
        sat__sorted = dict()
        sun__sorted = dict()

        for key in sorted(sat_.keys()):
            sat__sorted[key] = sat_[key]
        for key in sorted(sun_.keys()):
            sun__sorted[key] = sun_[key]

        context['sat'] = sat__sorted
        context['sun'] = sun__sorted
        KST, now = get_KST_now()
        if now.date() == datetime.date(2020, 9, 27):
            context['sunday'] = True

        for time in sat__sorted.keys():
            time = (time + datetime.timedelta(hours=9)).replace(tzinfo=KST)
            if ProgramCategory.objects.filter(slug="opening").exists():
                if sat__sorted[time][0] != '' and sat__sorted[time][0].category == ProgramCategory.objects.get(
                        slug="opening"):
                    if time < now < time + datetime.timedelta(minutes=10):
                        context['live'] = time
                        context['live_weekday'] = 5
                else:
                    if time < now < time + datetime.timedelta(minutes=40):
                        context['live'] = time
                        context['live_weekday'] = 5
            else:
                if time < now < time + datetime.timedelta(minutes=40):
                    context['live'] = time
                    context['live_weekday'] = 5

        for time in sun__sorted.keys():
            time = (time + datetime.timedelta(hours=9)).replace(tzinfo=KST)
            if time < now < time + datetime.timedelta(minutes=40):
                context['live'] = time
                context['live_weekday'] = 6

        try:
            context['keynote'] = ProgramCategory.objects.get(slug="keynote")
            context['lt'] = ProgramCategory.objects.get(slug="lightning_talk")
            context['opening'] = ProgramCategory.objects.get(slug="opening")
            context['closing'] = ProgramCategory.objects.get(slug="closing")
            context['pkot'] = ProgramCategory.objects.get(slug="pycon_korea_organizing_team")
        except ProgramCategory.DoesNotExist:
            pass

        context['track1'] = constance.config.YOUTUBE_TRACK_1
        context['track2'] = constance.config.YOUTUBE_TRACK_2
        context['track3'] = constance.config.YOUTUBE_TRACK_3
        context['track4'] = constance.config.YOUTUBE_TRACK_4
        context['track5'] = constance.config.YOUTUBE_TRACK_5
        context['lt1'] = constance.config.YOUTUBE_TRACK_LT_1
        context['lt2'] = constance.config.YOUTUBE_TRACK_LT_2
        context['closing_link'] = constance.config.YOUTUBE_TRACK_CLOSING

        return context


class ProposalCreate(SuccessMessageMixin, CreateView):
    form_class = ProposalForm
    template_name = "pyconkr/proposal_form.html"
    success_message = _("Proposal successfully created.")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(ProposalCreate, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        return super(ProposalCreate, self).get(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.profile.name == '':
            return redirect('profile_edit')

        EDIT_AVAILABLE = edit_proposal_available_checker(request)
        CFP_OPENED = is_proposal_opened(request)

        if CFP_OPENED == -1:
            return redirect("/2020/error/unopened")
        elif CFP_OPENED == 1 and EDIT_AVAILABLE is False:
            return redirect("/2020/error/closed/")

        return super(ProposalCreate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        new_cfp_registered(self.request.META['HTTP_ORIGIN'], self.object.id, self.object.title)
        return reverse('proposal-list')


class ProposalList(ListView):
    model = Proposal
    template_name = "pyconkr/proposal_list.html"

    def get_context_data(self, **kwargs):
        context = super(ProposalList, self).get_context_data(**kwargs)
        context['proposals'] = Proposal.objects.filter(user=self.request.user)
        context['is_proposable'] = is_proposal_opened(self.request) == 0
        if Proposal.objects.filter(user=self.request.user, accepted=True).exists():
            context['accepted_pk'] = Proposal.objects.get(user=self.request.user, accepted=True).pk

        return context

    def dispatch(self, request, *args, **kwargs):
        if not Proposal.objects.filter(user=self.request.user).exists():
            return redirect('propose')

        return super(ProposalList, self).dispatch(request, *args, **kwargs)


class ProposalUpdate(SuccessMessageMixin, UpdateView):
    model = Proposal
    form_class = ProposalForm
    template_name = "pyconkr/proposal_form.html"
    success_message = _("Proposal successfully updated.")

    def dispatch(self, request, *args, **kwargs):
        if edit_proposal_available_checker(request) is False:
            return redirect("/2020/error/closed/")

        return super(ProposalUpdate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProposalUpdate, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        cfp_updated(self.request.META['HTTP_ORIGIN'], self.object.id, self.object.title)
        return reverse('proposal', kwargs={'pk': self.object.id})


class ProposalDetail(DetailView):
    model = Proposal
    template_name = "pyconkr/proposal_detail.html"

    def dispatch(self, request, *args, **kwargs):
        if not Proposal.objects.filter(user=request.user).exists():
            return redirect('proposal-list')
        if Proposal.objects.get(id=self.kwargs['pk']).user != self.request.user:
            return redirect('proposal-list')
        return super(ProposalDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProposalDetail, self).get_context_data(**kwargs)
        context['title'] = _("Proposal")
        context['proposal'] = Proposal.objects.get(user=self.request.user, id=self.kwargs['pk'])
        context['is_editable'] = edit_proposal_available_checker(self.request)

        KST, now = get_KST_now()
        context['introduction_editable'] = now > constance.config.SCHEDULE_OPEN
        return context


class OpenReviewHome(TemplateView):
    template_name = "pyconkr/openreview_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        KST, now = get_KST_now()
        review_start_at = constance.config.OPEN_REVIEW_START.replace(tzinfo=KST)
        review_finish_at = constance.config.OPEN_REVIEW_FINISH.replace(tzinfo=KST)

        context['review_start_at'] = review_start_at
        context['review_finish_at'] = review_finish_at
        context['is_review_able'] = review_start_at < now < review_finish_at
        context['is_submitted'] = OpenReview.objects.filter(user=self.request.user, submitted=True).exists()
        return context


class OpenReviewList(TemplateView):
    template_name = "pyconkr/openreview_list.html"
    is_language = True  # 최초 시작시 언어 선택폼 부터 출력
    selected_language = None
    is_empty = False

    def post(self, request, *args, **kwargs):
        language_form = OpenReviewLanguageForm(request.POST)
        category_form = OpenReviewCategoryForm(request.POST)

        # 언어선택폼 처리의 경우
        if language_form.is_valid():
            self.is_language = False  # 다음 페이지에서는 카테코리 선택 폼을 출력
            self.selected_language = language_form.cleaned_data['language']

        # 카테고리 지정 폼을 처리하는 경우, 이미 지정된 오픈리뷰가 없는 경우
        if category_form.is_valid() and not OpenReview.objects.filter(user=request.user):
            category_id = category_form.cleaned_data['category'].id
            language = request.POST['selected_language']

            if request.POST['selected_language'] == 'N':
                ids = Proposal.objects \
                    .filter(category_id=category_id) \
                    .exclude(user=self.request.user) \
                    .values_list('id', flat=True)
            else:
                ids = Proposal.objects \
                    .filter(category_id=category_id, language=language) \
                    .exclude(user=request.user) \
                    .values_list('id', flat=True)
            if not ids.exists():
                self.is_empty = True

            # 랜덤 추출
            selected_ids = random.sample(list(ids), min(len(ids), 4))

            # 추출건 저장
            for proposal in Proposal.objects.filter(id__in=selected_ids):
                review = OpenReview(proposal=proposal, user=request.user, category_id=category_id)
                review.save()

        context = self.get_context_data()
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super(OpenReviewList, self).get_context_data(**kwargs)
        if self.is_language is True:
            context['is_language'] = True
        else:
            context['is_language'] = False

        # 리뷰할 CFP가 없을 때
        if self.is_empty:
            context['is_empty'] = True

        # 이미 리뷰할 CFP가 지정된 경우
        if OpenReview.objects.filter(user=self.request.user).exists():
            context['reviews'] = OpenReview.objects.filter(user=self.request.user).all()
        else:
            # 언어선택 폼
            context['select_language'] = OpenReviewLanguageForm()

            # 카테고리 선택 폼
            category_form = OpenReviewCategoryForm()
            category_form.helper.add_input(Hidden(name='selected_language', value=self.selected_language))

            context['select_category'] = category_form

        # 모든 리뷰를 작성했는지 확인
        for review in OpenReview.objects.filter(user=self.request.user):
            if review.comment == "":
                context['all_reviewed'] = False
                return context
        context['all_reviewed'] = True

        return context


class OpenReviewUpdate(UpdateView):
    model = OpenReview
    form_class = OpenReviewCommentForm
    template_name = "pyconkr/openreview_form.html"

    def get(self, request, *args, **kwargs):
        open_review_flag = is_open_review_opened()

        review = OpenReview.objects.get(id=self.kwargs['pk'])
        if review.user != self.request.user:
            return redirect('openreview')
        elif review.user == self.request.user and review.submitted:
            return redirect('openreview')

        if open_review_flag == -1:
            return redirect('/2020/error/unopened')
        elif open_review_flag == 0:
            return super().get(request, *args, **kwargs)
        else:
            return redirect('/2020/error/closed/')

    def get_context_data(self, **kwargs):
        context = super(OpenReviewUpdate, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('openreview-list')


class OpenReviewResult(ListView):
    model = OpenReview
    template_name = "pyconkr/openreview_result.html"

    def get(self, request, *args, **kwargs):
        reviews = OpenReview.objects.filter(user=self.request.user)
        for review in reviews:
            if review.comment == "":
                return redirect('openreview')

        for review in reviews:
            review.submitted = True
            review.save()

        return super().get(request, *args, **kwargs)


def edit_proposal_available_checker(request):
    KST, now = get_KST_now()
    flag = False  # 아래에 지정된 상황이 아니면 CFP Closed 상태

    cfp_open = constance.config.CFP_OPEN.replace(tzinfo=KST)
    cfp_close = constance.config.CFP_CLOSE.replace(tzinfo=KST)
    open_review_start = constance.config.OPEN_REVIEW_START.replace(tzinfo=KST)
    open_review_finish = constance.config.OPEN_REVIEW_FINISH.replace(tzinfo=KST)
    schedule_open = constance.config.SCHEDULE_OPEN.replace(tzinfo=KST)

    # CFP 마감 후 오픈리뷰 시작 전
    if cfp_close < now < open_review_start and Proposal.objects.filter(user=request.user).exists():
        print('제출한 CFP가 있는 경우, 오픈리뷰 시작 전에는 수정 가능')
        flag = True
    # 오픈리뷰 종료 후
    elif open_review_finish < now and Proposal.objects.filter(user=request.user).exists():
        print('제출한 CFP가 있는 경우, 오픈리뷰 마감 후에는 수정 가능')
        flag = True
    elif cfp_open < now < cfp_close:
        print('CFP 제출 기간에는 수정 가능')
        flag = True
    # 발표 시간표 공개 후 불가능
    if now > schedule_open:
        print('발표 시간표 공개 후에는 수정 불가능, 발표 소개 업데이트 폼으로 수정 가능')
        flag = False
    return flag


def is_proposal_opened(request):
    KST, now = get_KST_now()
    cfp_open = constance.config.CFP_OPEN.replace(tzinfo=KST)
    cfp_close = constance.config.CFP_CLOSE.replace(tzinfo=KST)
    flag = 0

    # CFP 오픈 이전
    if cfp_open > now:
        flag = -1
    # CFP 마감 이후
    elif now > cfp_close:
        flag = 1
    return flag


def is_open_review_opened():
    # 현재시간
    KST, now = get_KST_now()

    open_review_start = constance.config.OPEN_REVIEW_START.replace(tzinfo=KST)
    open_review_deadline = constance.config.OPEN_REVIEW_FINISH.replace(tzinfo=KST)

    if now < open_review_start:
        return -1
    elif open_review_start < now < open_review_deadline:
        return 0
    else:
        return 1


def is_lightning_talk_proposable(request):
    KST, now = get_KST_now()
    LT_open_at = constance.config.LIGHTNING_TALK_OPEN.replace(tzinfo=KST)
    LT_close_at = constance.config.LIGHTNING_TALK_CLOSE.replace(tzinfo=KST)
    LT_N = constance.config.LIGHTNING_TALK_N
    if now < LT_open_at or now > LT_close_at:
        return False
    elif len(LightningTalk.objects.filter(day=1)) >= LT_N and len(LightningTalk.objects.filter(day=2)) >= LT_N:
        return False
    else:
        return True


def is_program_opened():
    KST, now = get_KST_now()
    program_open = constance.config.PROGRAM_OPEN.replace(tzinfo=KST)

    if now < program_open:
        return False
    else:
        return True


class LightningTalkHome(TemplateView):
    template_name = "pyconkr/lightning_talk_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        KST, now = get_KST_now()
        context['LT_open_at'] = constance.config.LIGHTNING_TALK_OPEN.replace(tzinfo=KST)
        context['LT_close_at'] = constance.config.LIGHTNING_TALK_CLOSE.replace(tzinfo=KST)
        context['is_open'] = now > constance.config.LIGHTNING_TALK_OPEN.replace(tzinfo=KST)
        context['is_proposable'] = is_lightning_talk_proposable(self.request)
        return context


class LightningTalkCreate(CreateView):
    form_class = LightningTalkForm
    template_name = "pyconkr/lightning_talk_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        return super(LightningTalkCreate, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        return super(LightningTalkCreate, self).get(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.profile.name == '':
            return redirect('profile_edit')

        if not is_lightning_talk_proposable(self.request):
            return redirect('lightning-talk')

        if LightningTalk.objects.filter(owner=self.request.user).exists():
            return redirect('lightning-talk-detail')

        return super(LightningTalkCreate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('lightning-talk-detail')


class LightningTalkDetail(TemplateView):
    template_name = "pyconkr/lightning_talk_detail.html"

    def dispatch(self, request, *args, **kwargs):
        if not LightningTalk.objects.filter(owner=self.request.user).exists():
            return redirect('lightning-talk')
        return super(LightningTalkDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LightningTalkDetail, self).get_context_data(**kwargs)
        context['title'] = _("Lightning Talk Proposal")
        context['talk'] = LightningTalk.objects.get(owner=self.request.user)
        context['is_editable'] = is_lightning_talk_proposable(self.request)
        return context


class LightningTalkUpdate(UpdateView):
    model = LightningTalk
    form_class = LightningTalkForm
    template_name = "pyconkr/lightning_talk_form.html"

    def dispatch(self, request, *args, **kwargs):
        if not LightningTalk.objects.filter(owner=self.request.user).exists() or not is_lightning_talk_proposable(
                self.request):
            return redirect('lightning-talk')
        if LightningTalk.objects.get(id=self.kwargs['pk']).owner != self.request.user:
            return redirect('lightning-talk')

        return super(LightningTalkUpdate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LightningTalkUpdate, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('lightning-talk-detail')


class SprintList(ListView):
    model = Sprint
    template_name = "pyconkr/sprint_list.html"


class KeynoteList(ListView):
    queryset = Proposal.objects.filter(category__slug="keynote")
    template_name = "pyconkr/keynote_list.html"

    def get_context_data(self, **kwargs):
        context = super(KeynoteList, self).get_context_data(**kwargs)
        KST, now = get_KST_now()
        if now > constance.config.KEYNOTE_OPEN:
            context['is_open'] = True
        return context


class ProgramRedirect(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        KST, now = get_KST_now()
        sat_close = datetime.datetime(2020, 9, 26, 17, 15, tzinfo=KST)
        sun_close = datetime.datetime(2020, 9, 27, 17, 0, tzinfo=KST)
        room = self.kwargs['room']
        day = self.kwargs['day']
        rooms = ['101', '102', '103', '104', '105']
        days = ['sat', 'sun']
        if room not in rooms or day not in days:
            raise Http404

        if now < sat_close:
            if day == 'sat':
                if room == '101' and constance.config.YOUTUBE_TRACK_1:
                    return redirect(constance.config.YOUTUBE_TRACK_1)
                elif room == '102' and constance.config.YOUTUBE_TRACK_2:
                    return redirect(constance.config.YOUTUBE_TRACK_2)
                elif room == '103' and constance.config.YOUTUBE_TRACK_3:
                    return redirect(constance.config.YOUTUBE_TRACK_3)
                elif room in ['104', '105']:
                    raise Http404
                else:  # 링크가 없는 경우
                    return render(request, 'base.html', {'title': '영상을 찾을 수 없습니다.',
                                                         'base_content': '영상이 아직 준비되지 않았습니다.'})
            elif day == 'sun':
                if room in ['101', '102', '103']:
                    raise Http404
                else:
                    return render(request, 'base.html', {'title': '영상을 찾을 수 없습니다.',
                                                         'base_content': '영상이 공개 중인 시간이 아닙니다.'})
        elif now < sun_close:
            if day == 'sat':
                if room in ['104', '105']:
                    raise Http404
                else:
                    return render(request, 'base.html', {'title': '영상을 찾을 수 없습니다.',
                                                         'base_content': '영상이 공개 중인 시간이 아닙니다.'})
            elif day == 'sun':
                if room == '104' and constance.config.YOUTUBE_TRACK_4:
                    return redirect(constance.config.YOUTUBE_TRACK_4)
                elif room == '105' and constance.config.YOUTUBE_TRACK_5:
                    return redirect(constance.config.YOUTUBE_TRACK_5)
                elif room in ['101', '102', '103']:
                    raise Http404
                else:  # 링크가 없는 경우
                    return render(request, 'base.html', {'title': '영상을 찾을 수 없습니다.',
                                                         'base_content': '영상이 아직 준비되지 않았습니다.'})
        else:
            if (day == 'sat' and room in ['104', '105']) or (day == 'sun' and room in ['101', '102', '103']):
                raise Http404
            else:
                return render(request, 'base.html', {'title': '행사가 종료되었습니다.',
                                                     'base_content': '영상 공개가 끝났습니다. 개별 영상은 이후 유튜브에 업로드될 예정입니다.'})


class LightningTalkRedirect(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        try:
            lt = ProgramCategory.objects.get(slug="lightning_talk")
        except ProgramCategory.DoesNotExist:
            return render(request, 'base.html', {'title': '영상을 찾을 수 없습니다.',
                                                 'base_content': '영상이 아직 준비되지 않았습니다.'})
        KST, now = get_KST_now()
        day = self.kwargs['day']
        days = ['sat', 'sun']
        if day not in days:
            raise Http404

        if Proposal.objects.filter(category=lt).exists():
            talks = Proposal.objects.filter(category=lt)
            for talk in talks:
                time = talk.video_open_at
                time = (time + datetime.timedelta(hours=9)).replace(tzinfo=KST)
                if now < time + datetime.timedelta(minutes=20):
                    if time.weekday() == 5:  # Saturday
                        if day == 'sat' and constance.config.YOUTUBE_TRACK_LT_1:
                            return redirect(constance.config.YOUTUBE_TRACK_LT_1)
                        elif day == 'sun':
                            return render(request, 'base.html', {'title': '영상을 찾을 수 없습니다.',
                                                                 'base_content': '영상이 공개 중인 시간이 아닙니다.'})
                        else:  # 링크가 없는 경우
                            return render(request, 'base.html', {'title': '영상을 찾을 수 없습니다.',
                                                                 'base_content': '영상이 아직 준비되지 않았습니다.'})
                    elif time.weekday() == 6:  # Sunday
                        if now.weekday() == 6 and day == 'sun' and constance.config.YOUTUBE_TRACK_LT_2:
                            return redirect(constance.config.YOUTUBE_TRACK_LT_2)
                        elif now.weekday() != 6:
                            return render(request, 'base.html', {'title': '영상을 찾을 수 없습니다.',
                                                                 'base_content': '영상이 공개 중인 시간이 아닙니다.'})
                        else:
                            return render(request, 'base.html', {'title': '영상을 찾을 수 없습니다.',
                                                                 'base_content': '영상이 아직 준비되지 않았습니다.'})
            return render(request, 'base.html', {'title': '행사가 종료되었습니다.',
                                                 'base_content': '영상 공개가 끝났습니다. 개별 영상은 이후 유튜브에 업로드될 예정입니다.'})
        else:
            return render(request, 'base.html', {'title': '영상을 찾을 수 없습니다.',
                                                 'base_content': '영상이 아직 준비되지 않았습니다.'})


class ClosingRedirect(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        try:
            closing = Proposal.objects.get(category=ProgramCategory.objects.get(slug="closing"))
        except ProgramCategory.DoesNotExist or Proposal.DoesNotExist:
            return render(request, 'base.html', {'title': '영상을 찾을 수 없습니다.',
                                                 'base_content': '영상이 아직 준비되지 않았습니다.'})

        KST, now = get_KST_now()
        time = closing.video_open_at
        time = (time + datetime.timedelta(hours=9)).replace(tzinfo=KST)
        if now < time + datetime.timedelta(minutes=20):
            if constance.config.YOUTUBE_TRACK_CLOSING:
                return redirect(constance.config.YOUTUBE_TRACK_CLOSING)
            else:
                return render(request, 'base.html', {'title': '영상을 찾을 수 없습니다.',
                                                     'base_content': '영상이 아직 준비되지 않았습니다.'})
        else:
            return render(request, 'base.html', {'title': '행사가 종료되었습니다.',
                                                 'base_content': '영상 공개가 끝났습니다. 개별 영상은 이후 유튜브에 업로드될 예정입니다.'})
