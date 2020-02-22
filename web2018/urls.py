from django.conf import settings
from django.conf.urls import include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib.flatpages import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from django.urls import re_path
# from web2018 import TutorialProposalCreate, TutorialProposalDetail, \
#     TutorialProposalUpdate, TutorialProposalList, SprintProposalList, tutorial_join,\
#     SprintProposalCreate, SprintProposalDetail, sprint_join, SprintProposalUpdate

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

# for development
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
