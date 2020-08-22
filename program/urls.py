from django.contrib.auth.decorators import login_required
from django.urls import re_path
from .views import ProgramList
from .views import ProposalCreate, ProposalUpdate, ProposalDetail, ProposalList

from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    re_path(r'^talks/$',
            ProgramList.as_view(), name='programs'),
    re_path(r'^cfp/propose/$',
            login_required(ProposalCreate.as_view()), name='propose'),
    re_path(r'^profile/proposal/(?P<pk>\d+)$',
            login_required(ProposalDetail.as_view()), name='proposal'),
    re_path(r'^profile/proposal/list',
            login_required(ProposalList.as_view()), name='proposal-list'),

    re_path(r'^profile/proposal/(?P<pk>\d+)/edit$',
            login_required(ProposalUpdate.as_view()), name='proposal-update'),
]
