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
    re_path(r'^2020/robots.txt$', robots, name='robots'),
    re_path(r'2020/summernote/', include('django_summernote.urls')),
    re_path(r'^2020/admin/', admin.site.urls),

    re_path(r'^2020/accounts/', include('allauth.urls')),
    re_path(r'^2020/i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    re_path(r'^2020/$', index, name='index'),
    re_path(r'^2020/room/(?P<pk>\d+)$',
            RoomDetail.as_view(), name='room'),

    re_path(r'^2020/about/announcements/$',
            AnnouncementList.as_view(), name='announcements'),
    re_path(r'^2020/about/announcement/(?P<pk>\d+)$',
            AnnouncementDetail.as_view(), name='announcement'),
    re_path(r'^2020/about/sponsor/$',
            SponsorList.as_view(), name='sponsors'),
    re_path(r'^2020/about/patron/$',
            PatronList.as_view(), name='patrons'),
    re_path(r'^2020/about/sponsor/(?P<slug>[\w|-]+)$',
            SponsorDetail.as_view(), name='sponsor'),

    re_path(r'^2020/programs?/list/$',
            ProgramList.as_view(), name='programs'),
    re_path(r'^2020/programs?/preference/$',
            login_required(PreferenceList.as_view()), name='program_preference'),
    re_path(r'^2020/program/(?P<pk>\d+)$',
            ProgramDetail.as_view(), name='program'),
    re_path(r'^2020/program/(?P<pk>\d+)/edit$',
            ProgramUpdate.as_view(), name='program_edit'),
    re_path(r'^2020/programs?/speakers?/$',
            SpeakerList.as_view(), name='speakers'),
    re_path(r'^2020/programs?/speakers?/(?P<slug>\w+)$',
            SpeakerDetail.as_view(), name='speaker'),
    re_path(r'^2020/programs?/speakers?/(?P<slug>\w+)/edit$',
            SpeakerUpdate.as_view(), name='speaker_edit'),
    re_path(r'^2020/programs?/schedule/$',
            schedule, name='schedule'),
    re_path(r'^2020/programs?/youngcoder/$',
            youngcoder, name='youngcoder'),
    re_path(r'^2020/programs?/child_care/$',
            child_care, name='child_care'),
    re_path(r'^2020/programs?/tutorial/$',
            TutorialProposalList.as_view(), name='tutorial'),
    re_path(r'^2020/programs?/sprint/$',
            SprintProposalList.as_view(), name='sprint'),
    re_path(r'^2020/programs?/tutorial/(?P<pk>\d+)$',
            TutorialProposalDetail.as_view(), name='tutorial'),
    re_path(r'^2020/programs?/tutorial/(?P<pk>\d+)/join/$',
            login_required(tutorial_join), name='tutorial-join'),
    re_path(r'^2020/programs?/sprint/(?P<pk>\d+)$',
            SprintProposalDetail.as_view(), name='sprint'),
    re_path(r'^2020/programs?/sprint/(?P<pk>\d+)/join/$',
            login_required(sprint_join), name='sprint-join'),

    re_path(r'^2020/cfp/propose/$',
            login_required(ProposalCreate.as_view()), name='propose'),
    re_path(r'^2020/cfp/tutorial-propose/$',
            login_required(TutorialProposalCreate.as_view()), name='tutorial-propose'),
    re_path(r'^2020/profile/proposal/$',
            login_required(ProposalDetail.as_view()), name='proposal'),
    re_path(r'^2020/cfp/sprint-propose/$',
            login_required(SprintProposalCreate.as_view()), name='sprint-propose'),

    re_path(r'^2020/profile/proposal/edit$',
            login_required(ProposalUpdate.as_view()), name='proposal-update'),
    re_path(r'^2020/profile/tutorial-proposal/edit$',
            login_required(TutorialProposalUpdate.as_view()), name='tutorial-proposal-update'),
    re_path(r'^2020/profile/sprint-proposal/edit$',
            login_required(SprintProposalUpdate.as_view()), name='sprint-proposal-update'),
    re_path(r'^2020/profile$',
            login_required(ProfileDetail.as_view()), name='profile'),
    re_path(r'^2020/profile/edit$',
            login_required(ProfileUpdate.as_view()), name='profile_edit'),

    re_path(r'^2020/login/$', login, name='login'),
    re_path(r'^2020/login/req/(?P<token>[a-z0-9\-]+)$',
            login_req, name='login_req'),
    re_path(r'^2020/login/mailsent/$', login_mailsent, name='login_mailsent'),
    re_path(r'^2020/logout/$', logout, name='logout'),

    re_path(r'^2020/registration/', include('registration.urls')),

    # for rosetta
    re_path(r'^2020/rosetta/', include('rosetta.urls')),

    # for flatpages
    re_path(r'^2020/pages/', include('django.contrib.flatpages.urls')),
    re_path(r'^2020/(?P<url>.*/)$', views.flatpage, name='flatpage'),

    prefix_default_language=False
)

# for development
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
