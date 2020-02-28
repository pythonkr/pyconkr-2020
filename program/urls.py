from django.contrib.auth.decorators import login_required
from django.urls import re_path
from .views import (ProgramList, PreferenceList, ProgramDetail, ProgramUpdate,
                    SpeakerList, SpeakerUpdate, SpeakerDetail,
                    SprintProposalCreate, SprintProposalList, SprintProposalDetail, SprintProposalUpdate,
                    TutorialProposalCreate, TutorialProposalList, TutorialProposalDetail, TutorialProposalUpdate,
                    RoomDetail)
from .views import ProposalCreate, ProposalUpdate, ProposalDetail
from .views import schedule, youngcoder, child_care, tutorial_join, sprint_join

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    re_path(r'^list/$',
            ProgramList.as_view(), name='programs'),
    re_path(r'^preference/$',
            login_required(PreferenceList.as_view()), name='program_preference'),
    re_path(r'^(?P<pk>\d+)$',
            ProgramDetail.as_view(), name='program'),
    re_path(r'^(?P<pk>\d+)/edit$',
            ProgramUpdate.as_view(), name='program_edit'),
    re_path(r'^speakers?/$',
            SpeakerList.as_view(), name='speakers'),
    re_path(r'^speakers?/(?P<slug>\w+)$',
            SpeakerDetail.as_view(), name='speaker'),
    re_path(r'^speakers?/(?P<slug>\w+)/edit$',
            SpeakerUpdate.as_view(), name='speaker_edit'),
    re_path(r'^schedule/$',
            schedule, name='schedule'),
    re_path(r'^youngcoder/$',
            youngcoder, name='youngcoder'),
    re_path(r'^child_care/$',
            child_care, name='child_care'),
    re_path(r'^tutorial/$',
            TutorialProposalList.as_view(), name='tutorial'),
    re_path(r'^sprint/$',
            SprintProposalList.as_view(), name='sprint'),
    re_path(r'^tutorial/(?P<pk>\d+)$',
            TutorialProposalDetail.as_view(), name='tutorial'),
    re_path(r'^tutorial/(?P<pk>\d+)/join/$',
            login_required(tutorial_join), name='tutorial-join'),
    re_path(r'^sprint/(?P<pk>\d+)$',
            SprintProposalDetail.as_view(), name='sprint'),
    re_path(r'^sprint/(?P<pk>\d+)/join/$',
            login_required(sprint_join), name='sprint-join'),
    re_path(r'^room/(?P<pk>\d+)$',
            RoomDetail.as_view(), name='room'),

    re_path(r'^cfp/propose/$',
            login_required(ProposalCreate.as_view()), name='propose'),
    re_path(r'^cfp/tutorial-propose/$',
            login_required(TutorialProposalCreate.as_view()), name='tutorial-propose'),
    re_path(r'^profile/proposal/$',
            login_required(ProposalDetail.as_view()), name='proposal'),
    re_path(r'^cfp/sprint-propose/$',
            login_required(SprintProposalCreate.as_view()), name='sprint-propose'),

    re_path(r'^profile/proposal/edit$',
            login_required(ProposalUpdate.as_view()), name='proposal-update'),
    re_path(r'^profile/tutorial-proposal/edit$',
            login_required(TutorialProposalUpdate.as_view()), name='tutorial-proposal-update'),
    re_path(r'^profile/sprint-proposal/edit$',
            login_required(SprintProposalUpdate.as_view()), name='sprint-proposal-update'),
]
