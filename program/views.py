import random

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, CreateView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext as _
from django.urls import reverse
from django.views.generic.edit import ModelFormMixin

from crispy_forms.layout import Hidden

from .models import Program, ProgramCategory, Preference, Speaker, Room, Proposal, OpenReview, \
    TutorialProposal, SprintProposal, LightningTalk
from .forms import SpeakerForm, SprintProposalForm, TutorialProposalForm, ProposalForm, \
    OpenReviewCategoryForm, OpenReviewCommentForm, OpenReviewLanguageForm, ProgramForm
    OpenReviewCategoryForm, OpenReviewCommentForm, OpenReviewLanguageForm, ProgramForm, LightningTalkForm

import constance
import datetime

from program.slack import new_cfp_registered, cfp_updated


class ContributionHome(TemplateView):
    template_name = "pyconkr/contribution_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        KST = datetime.timezone(datetime.timedelta(hours=9))
        now = datetime.datetime.now(tz=KST)
        context['cfp_open'] = constance.config.CFP_OPEN.replace(tzinfo=KST)
        context['cfp_close'] = constance.config.CFP_CLOSE.replace(tzinfo=KST)
        context['keynote_start_at'] = constance.config.KEYNOTE_RECOMMEND_OPEN.replace(tzinfo=KST)
        context['keynote_end_at'] = constance.config.KEYNOTE_RECOMMEND_CLOSE.replace(tzinfo=KST)
        context['review_start_at'] = constance.config.OPEN_REVIEW_START.replace(tzinfo=KST)
        context['review_finish_at'] = constance.config.OPEN_REVIEW_FINISH.replace(tzinfo=KST)
        context['lightning_talk_open'] = constance.config.LIGHTNING_TALK_OPEN.replace(tzinfo=KST)
        context['lightning_talk_close'] = constance.config.LIGHTNING_TALK_CLOSE.replace(
            tzinfo=KST)
        context['now'] = now

        return context


class ProgramList(ListView):
    model = ProgramCategory
    template_name = "pyconkr/program_list.html"


class ProgramDetail(DetailView):
    model = Program

    def get_context_data(self, **kwargs):
        context = super(ProgramDetail, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            for speaker in self.object.speakers.all():
                if self.request.user.email == speaker.email:
                    context['editable'] = True

        return context


class PreferenceList(SuccessMessageMixin, ListView):
    model = Preference
    template_name = "pyconkr/program_preference.html"

    def get_queryset(self):
        queryset = super(PreferenceList, self).get_queryset()
        return queryset.filter(user=self.request.user).values_list('program', flat=True)

    def post(self, request, **kwargs):
        Preference.objects.filter(user=request.user).delete()

        preferences = []
        for program_id in request.POST.getlist('program[]')[:5]:
            preferences.append(Preference(
                user=request.user,
                program=Program.objects.get(id=program_id)))

        Preference.objects.bulk_create(preferences)
        messages.success(self.request, _(
            "Preferences are successfully updated."))
        return super(PreferenceList, self).get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PreferenceList, self).get_context_data(**kwargs)

        # Shuffle programs by user id
        programs = list(Program.objects.all())
        random.seed(self.request.user.id)
        random.shuffle(programs)

        context['programs'] = programs

        return context


class SpeakerList(ListView):
    model = Speaker


class RoomDetail(DetailView):
    model = Room


class SpeakerDetail(DetailView):
    model = Speaker

    def get_context_data(self, **kwargs):
        context = super(SpeakerDetail, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            if self.request.user.email == self.object.email:
                context['editable'] = True

        return context


class SpeakerUpdate(UpdateView):
    model = Speaker
    form_class = SpeakerForm

    def get_queryset(self):
        queryset = super(SpeakerUpdate, self).get_queryset()
        return queryset.filter(email=self.request.user.email)


def schedule(request):
    dates = ProgramDate.objects.all()
    times = ProgramTime.objects.order_by('begin')
    rooms = Room.objects.order_by('name')

    wide = {}
    narrow = {}
    processed = set()
    for d in dates:
        wide[d] = {}
        narrow[d] = {}
        for t in times:
            if t.day_id != d.id:
                continue
            wide[d][t] = {}
            narrow[d][t] = []
            for r in rooms:
                s = Program.objects.filter(date=d, times=t, rooms=r)

                if s:
                    s_times = s[0].get_sort_times()
                    if s_times.first() == t and s[0].id not in processed:
                        wide[d][t][r] = s[0]
                        narrow[d][t].append(s[0])
                        processed.add(s[0].id)
                else:
                    wide[d][t][r] = None

            if len(narrow[d][t]) == 0:
                del (narrow[d][t])

    contexts = {
        'wide': wide,
        'narrow': narrow,
        'rooms': rooms,
        'width': 100.0 / max(len(rooms), 1),
    }
    return render(request, 'schedule.html', contexts)


def youngcoder(request):
    contexts = {}
    return render(request, 'youngcoder.html', contexts)


def child_care(request):
    contexts = {}
    return render(request, 'child_care.html', contexts)


class TutorialProposalList(ListView):
    model = TutorialProposal

    def get_context_data(self, **kwargs):
        context = super(TutorialProposalList, self).get_context_data(**kwargs)
        context['tutorials'] = TutorialProposal.objects.filter(
            confirmed=True).all()
        return context


class SprintProposalList(ListView):
    model = SprintProposal

    def get_context_data(self, **kwargs):
        context = super(SprintProposalList, self).get_context_data(**kwargs)
        context['sprints'] = SprintProposal.objects.filter(
            confirmed=True).all()
        if self.request.user.is_authenticated:
            context['joined_tutorials'] = TutorialCheckin.objects.filter(user=self.request.user).values_list(
                'tutorial_id', flat=True)
        return context


def tutorial_join(request, pk):
    tutorial = get_object_or_404(TutorialProposal, pk=pk)

    if request.GET.get('leave'):
        TutorialCheckin.objects.filter(
            user=request.user, tutorial=tutorial).delete()
    else:
        tc = TutorialCheckin(user=request.user, tutorial=tutorial)
        tc.save()

    return redirect('tutorial', pk)


class SprintProposalDetail(DetailView):
    model = SprintProposal
    context_object_name = 'sprint'

    def get_context_data(self, **kwargs):
        context = super(SprintProposalDetail, self).get_context_data(**kwargs)
        checkin_ids = \
            SprintCheckin.objects.filter(sprint=self.object). \
                order_by('id').values_list('id', flat=True)
        limit_bar_id = 65539
        checkins = SprintCheckin.objects.filter(sprint=self.object)
        attendees = []
        for x in checkins:
            if not hasattr(x.user, 'profile'):
                attendees.append({'name': x.user.email.split('@')[0],
                                  'picture': None,
                                  'registered': Registration.objects.filter(user=x.user,
                                                                            payment_status='paid').exists(),
                                  'waiting': True if x.id > limit_bar_id else False
                                  })
            else:
                attendees.append({'name': x.user.profile.name if x.user.profile.name != '' else
                x.user.email.split('@')[0],
                                  'picture': x.user.profile.image,
                                  'registered':
                                      Registration.objects.filter(user=x.user,
                                                                  payment_status='paid').exists(),
                                  'waiting': True if x.id > limit_bar_id else False
                                  })
        context['attendees'] = attendees

        if self.request.user.is_authenticated:
            context['joined'] = \
                SprintCheckin.objects.filter(
                    user=self.request.user, sprint=self.object).exists()
        else:
            context['joined'] = False

        return context


class SprintProposalUpdate(SuccessMessageMixin, UpdateView):
    model = SprintProposal
    form_class = SprintProposalForm
    template_name = "pyconkr/proposal_form.html"
    success_message = _("Sprint proposal successfully updated.")

    def get_object(self, queryset=None):
        return get_object_or_404(SprintProposal, pk=self.request.user.sprintproposal.pk)

    def get_context_data(self, **kwargs):
        context = super(SprintProposalUpdate, self).get_context_data(**kwargs)
        context['title'] = _("Update sprint")
        return context

    def get_success_url(self):
        return reverse('sprint', args=(self.object.id,))


def sprint_join(request, pk):
    sprint = get_object_or_404(SprintProposal, pk=pk)

    if request.GET.get('leave'):
        SprintCheckin.objects.filter(user=request.user, sprint=sprint).delete()
    else:
        sc = SprintCheckin(user=request.user, sprint=sprint)
        sc.save()

    return redirect('sprint', pk)


class SprintProposalCreate(SuccessMessageMixin, CreateView):
    form_class = SprintProposalForm
    template_name = "pyconkr/proposal_form.html"
    success_message = _("Sprint proposal successfully created.")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(SprintProposalCreate, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        sprint = SprintProposal.objects.filter(user=request.user)
        if sprint.exists():
            return redirect('sprint', sprint.first().id)
        if request.user.profile.name == '':
            return redirect('profile_edit')
        return super(SprintProposalCreate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('sprint', args=(self.object.id,))


class TutorialProposalUpdate(SuccessMessageMixin, UpdateView):
    model = TutorialProposal
    form_class = TutorialProposalForm
    template_name = "pyconkr/proposal_form.html"
    success_message = _("Tutorial proposal successfully updated.")

    def get_object(self, queryset=None):
        return get_object_or_404(TutorialProposal, pk=self.request.user.tutorialproposal.pk)

    def get_context_data(self, **kwargs):
        context = super(TutorialProposalUpdate,
                        self).get_context_data(**kwargs)
        context['title'] = _("Update tutorial")
        return context

    def get_success_url(self):
        return reverse('tutorial', args=(self.object.id,))


class TutorialProposalDetail(DetailView):
    model = TutorialProposal
    context_object_name = 'tutorial'

    def get_context_data(self, **kwargs):
        context = super(TutorialProposalDetail,
                        self).get_context_data(**kwargs)
        capacity = self.object.capacity
        checkin_ids = \
            TutorialCheckin.objects.filter(tutorial=self.object). \
                order_by('id').values_list('id', flat=True)
        limit_bar_id = 65539
        if capacity < len(checkin_ids):
            limit_bar_id = checkin_ids[capacity - 1]
        attendees = [{'name': x.user.profile.name if x.user.profile.name != '' else
        x.user.email.split('@')[0],
                      'picture': x.user.profile.image,
                      'registered':
                          Registration.objects.filter(user=x.user,
                                                      payment_status='paid').exists(),
                      'waiting': True if x.id > limit_bar_id else False
                      } for x in TutorialCheckin.objects.filter(tutorial=self.object)]
        context['attendees'] = attendees

        if self.request.user.is_authenticated:
            context['joined'] = \
                TutorialCheckin.objects.filter(
                    user=self.request.user, tutorial=self.object).exists()
        else:
            context['joined'] = False

        if self.object.option:
            context['option'] = self.object.option

        if not self.request.user.is_anonymous:
            registration = Registration.objects.active_tutorial() \
                .filter(option=self.object.option, user=self.request.user, payment_status__in=['paid', 'ready'])
            if registration.exists():
                context['is_registered'] = True

        return context


class TutorialProposalCreate(SuccessMessageMixin, CreateView):
    form_class = TutorialProposalForm
    template_name = "pyconkr/proposal_form.html"
    success_message = _("Tutorial proposal successfully created.")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(TutorialProposalCreate, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        proposal = TutorialProposal.objects.filter(user=request.user)
        if proposal.exists():
            return redirect('tutorial', proposal.first().id)
        if request.user.profile.name == '':
            return redirect('profile_edit')
        return super(TutorialProposalCreate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('tutorial', args=(self.object.id,))


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
        context['EDIT_AVAILABLE'] = edit_proposal_available_checker(self.request)
        return context


class OpenReviewHome(TemplateView):
    template_name = "pyconkr/openreview_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        KST = datetime.timezone(datetime.timedelta(hours=9))
        now = datetime.datetime.now(tz=KST)
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

            if request.POST['selected_language'] == 'N':
                ids = Proposal.objects \
                    .filter(category_id=category_id) \
                    .exclude(user=self.request.user) \
                    .values_list('id', flat=True)
            else:
                ids = Proposal.objects \
                    .filter(category_id=category_id, language=request.POST['selected_language']) \
                    .exclude(user=request.user) \
                    .values_list('id', flat=True)
            if not ids.exists():
                self.is_empty = True

            # 랜덤 추출
            selected_ids = random.sample(list(ids), min(len(ids), 4))

            # 추출건 저장
            for proposal in Proposal.objects.filter(id__in=selected_ids):
                review = OpenReview(proposal=proposal, user=request.user)
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


class ProgramUpdate(UpdateView):
    model = Program
    form_class = ProgramForm

    def get_queryset(self):
        queryset = super(ProgramUpdate, self).get_queryset()
        return queryset.filter(speakers__email=self.request.user.email)


def edit_proposal_available_checker(request):
    KST = datetime.timezone(datetime.timedelta(hours=9))
    now = datetime.datetime.now(tz=KST)
    flag = False  # 아래에 지정된 상황이 아니면 CFP Closed 상태

    cfp_open = constance.config.CFP_OPEN.replace(tzinfo=KST)
    cfp_close = constance.config.CFP_CLOSE.replace(tzinfo=KST)
    open_review_start = constance.config.OPEN_REVIEW_START.replace(tzinfo=KST)
    open_review_finish = constance.config.OPEN_REVIEW_FINISH.replace(tzinfo=KST)

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

    return flag


def is_proposal_opened(request):
    KST = datetime.timezone(datetime.timedelta(hours=9))
    now = datetime.datetime.now(tz=KST)
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
    KST = datetime.timezone(datetime.timedelta(hours=9))
    now = datetime.datetime.now(tz=KST)

    open_review_start = constance.config.OPEN_REVIEW_START.replace(tzinfo=KST)
    open_review_deadline = constance.config.OPEN_REVIEW_FINISH.replace(tzinfo=KST)

    if now < open_review_start:
        return -1
    elif open_review_start < now < open_review_deadline:
        return 0
    else:
        return 1

def is_lightning_talk_proposable(request):
    KST = datetime.timezone(datetime.timedelta(hours=9))
    now = datetime.datetime.now(tz=KST)
    LT_open_at = constance.config.LIGHTNING_TALK_OPEN.replace(tzinfo=KST)
    LT_close_at = constance.config.LIGHTNING_TALK_CLOSE.replace(tzinfo=KST)
    if LT_open_at < now < LT_close_at:
        return True
    else:
        return False


class LightningTalkHome(TemplateView):
    template_name = "pyconkr/lightning_talk_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        KST = datetime.timezone(datetime.timedelta(hours=9))
        context['LT_open_at'] = constance.config.LIGHTNING_TALK_OPEN.replace(tzinfo=KST)
        context['LT_close_at'] = constance.config.LIGHTNING_TALK_CLOSE.replace(tzinfo=KST)
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
