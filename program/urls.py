from django.contrib.auth.decorators import login_required
from django.urls import re_path

from . import views

from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    re_path(r'^talks/$', views.ProgramList.as_view(), name='talk-list'),
    re_path(r'^talk/(?P<pk>\d+)$', views.ProgramDetail.as_view(), name='talk'),
    re_path(r'^talk/(?P<pk>\d+)/edit/$', login_required(views.ProgramUpdate.as_view()), name='talk-update'),
    re_path(r'^talk-schedule/$', views.ProgramSchedule.as_view(), name='talk-schedule'),
    re_path(r'^sprint/$', views.SprintList.as_view(), name='sprint'),
    re_path(r'^keynote/$', views.KeynoteList.as_view(), name='keynote'),
    re_path(r'^cfp/propose/$', login_required(views.ProposalCreate.as_view()), name='propose'),
    re_path(r'^profile/proposal/(?P<pk>\d+)$', login_required(views.ProposalDetail.as_view()), name='proposal'),
    re_path(r'^profile/proposal/list/$', login_required(views.ProposalList.as_view()), name='proposal-list'),
    re_path(r'^profile/proposal/(?P<pk>\d+)/edit/$', login_required(views.ProposalUpdate.as_view()), name='proposal-update'),
]
