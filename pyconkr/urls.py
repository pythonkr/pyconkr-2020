from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib.flatpages import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from django.views.generic.base import TemplateView
from pyconkr.views import TutorialProposalCreate, TutorialProposalDetail, \
    TutorialProposalUpdate, TutorialProposalList, SprintProposalList, tutorial_join,\
    SprintProposalCreate, SprintProposalDetail, sprint_join, SprintProposalUpdate

from .views import index, schedule, robots, youngcoder, child_care
from .views import RoomDetail
from .views import AnnouncementList, AnnouncementDetail
from .views import SpeakerList, SpeakerDetail, SpeakerUpdate
from .views import SponsorList, SponsorDetail, PatronList
from .views import ProgramList, ProgramDetail, ProgramUpdate, PreferenceList
from .views import ProposalCreate, ProposalUpdate, ProposalDetail
from .views import ProfileDetail, ProfileUpdate
from .views import login, login_req, login_mailsent, logout

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    re_path(r'^robots.txt$', robots, name='robots'),
    re_path(r'summernote/', include('django_summernote.urls')),
    re_path(r'^admin/', admin.site.urls),

    re_path(r'^accounts/', include('allauth.urls')),
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    re_path(r'^$', index, name='index'),
    re_path(r'^room/(?P<pk>\d+)$',
        RoomDetail.as_view(), name='room'),

    re_path(r'^about/announcements/$',
        AnnouncementList.as_view(), name='announcements'),
    re_path(r'^about/announcement/(?P<pk>\d+)$',
        AnnouncementDetail.as_view(), name='announcement'),
    re_path(r'^about/sponsor/$',
        SponsorList.as_view(), name='sponsors'),
    re_path(r'^about/patron/$',
        PatronList.as_view(), name='patrons'),
    re_path(r'^about/sponsor/(?P<slug>[\w|-]+)$',
        SponsorDetail.as_view(), name='sponsor'),

    re_path(r'^programs?/list/$',
        ProgramList.as_view(), name='programs'),
    re_path(r'^programs?/preference/$',
        login_required(PreferenceList.as_view()), name='program_preference'),
    re_path(r'^program/(?P<pk>\d+)$',
        ProgramDetail.as_view(), name='program'),
    re_path(r'^program/(?P<pk>\d+)/edit$',
        ProgramUpdate.as_view(), name='program_edit'),
    re_path(r'^programs?/speakers?/$',
        SpeakerList.as_view(), name='speakers'),
    re_path(r'^programs?/speakers?/(?P<slug>\w+)$',
        SpeakerDetail.as_view(), name='speaker'),
    re_path(r'^programs?/speakers?/(?P<slug>\w+)/edit$',
        SpeakerUpdate.as_view(), name='speaker_edit'),
    re_path(r'^programs?/schedule/$',
        schedule, name='schedule'),
    re_path(r'^programs?/youngcoder/$',
        youngcoder, name='youngcoder'),
    re_path(r'^programs?/child_care/$',
        child_care, name='child_care'),
    re_path(r'^programs?/tutorial/$',
        TutorialProposalList.as_view(), name='tutorial'),
    re_path(r'^programs?/sprint/$',
        SprintProposalList.as_view(), name='sprint'),
    re_path(r'^programs?/tutorial/(?P<pk>\d+)$',
        TutorialProposalDetail.as_view(), name='tutorial'),
    re_path(r'^programs?/tutorial/(?P<pk>\d+)/join/$',
        login_required(tutorial_join), name='tutorial-join'),
    re_path(r'^programs?/sprint/(?P<pk>\d+)$',
        SprintProposalDetail.as_view(), name='sprint'),
    re_path(r'^programs?/sprint/(?P<pk>\d+)/join/$',
        login_required(sprint_join), name='sprint-join'),

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
    re_path(r'^profile$',
        login_required(ProfileDetail.as_view()), name='profile'),
    re_path(r'^profile/edit$',
        login_required(ProfileUpdate.as_view()), name='profile_edit'),

    re_path(r'^login/$', login, name='login'),
    re_path(r'^login/req/(?P<token>[a-z0-9\-]+)$', login_req, name='login_req'),
    re_path(r'^login/mailsent/$', login_mailsent, name='login_mailsent'),
    re_path(r'^logout/$', logout, name='logout'),

    re_path(r'^registration/', include('registration.urls')),
    re_path(r'^2020/', include('web2020.urls')),
    # for rosetta
    re_path(r'^rosetta/', include('rosetta.urls')),

    # for flatpages
    re_path(r'^pages/', include('django.contrib.flatpages.urls')),
    re_path(r'^(?P<url>.*/)$', views.flatpage, name='flatpage'),

    prefix_default_language=False
)

# for development
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
