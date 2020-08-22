from django.contrib.auth.decorators import login_required
from django.urls import re_path
from .views import (ProgramList, PreferenceList, ProgramDetail, ProgramUpdate,
                    SpeakerList, SpeakerUpdate, SpeakerDetail)
from .views import ProposalCreate, ProposalUpdate, ProposalDetail, ProposalList
from .views import schedule

from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    re_path(r'^talks/$',
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
    re_path(r'^cfp/propose/$',
            login_required(ProposalCreate.as_view()), name='propose'),
    re_path(r'^profile/proposal/(?P<pk>\d+)$',
            login_required(ProposalDetail.as_view()), name='proposal'),
    re_path(r'^profile/proposal/list',
            login_required(ProposalList.as_view()), name='proposal-list'),

    re_path(r'^profile/proposal/(?P<pk>\d+)/edit$',
            login_required(ProposalUpdate.as_view()), name='proposal-update'),
]
