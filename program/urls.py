from django.contrib.auth.decorators import login_required
from django.urls import re_path
from .views import ProgramList, ProgramDetail
from .views import ProposalCreate, ProposalUpdate, ProposalDetail, ProposalList, ProgramUpdate, ProgramSchedule, \
    SprintList, KeynoteList

from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    re_path(r'^talks/$',
            ProgramList.as_view(), name='talk-list'),
    re_path(r'^talk/(?P<pk>\d+)$',
            ProgramDetail.as_view(), name='talk'),
    re_path(r'^talk/(?P<pk>\d+)/edit$',
            login_required(ProgramUpdate.as_view()), name='talk-update'),
    re_path(r'^talk-schedule/$', ProgramSchedule.as_view(), name='talk-schedule'),
    re_path(r'^sprint/$', SprintList.as_view()),
    re_path(r'^keynote/$', KeynoteList.as_view()),
    re_path(r'^cfp/propose/$',
            login_required(ProposalCreate.as_view()), name='propose'),
    re_path(r'^profile/proposal/(?P<pk>\d+)$',
            login_required(ProposalDetail.as_view()), name='proposal'),
    re_path(r'^profile/proposal/list',
            login_required(ProposalList.as_view()), name='proposal-list'),
    re_path(r'^profile/proposal/(?P<pk>\d+)/edit$',
            login_required(ProposalUpdate.as_view()), name='proposal-update'),
]
