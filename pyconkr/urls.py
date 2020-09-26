from django.conf import settings
from django.conf.urls import include, url, handler404, handler500
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from django.urls import re_path, path
from django.views.generic import RedirectView

from constance import config

from .views import index, robots
from .views import login, logout

from program.views import OpenReviewUpdate, OpenReviewList, OpenReviewHome, OpenReviewResult, ContributionHome, \
    LightningTalkCreate, LightningTalkHome, LightningTalkDetail, LightningTalkUpdate, LightningTalkRedirect, \
    ClosingRedirect, ProgramRedirect
from registration.views import PatronList
from mailing.views import NewsLetterAdd, NewsLetterRemove, NewsLetterRemoveConfirm, SlackInvitation
from user.views import StaffList

admin.autodiscover()

urlpatterns = [
    re_path(r'^2020/robots.txt$', robots, name='robots'),
    re_path(r'^2020/summernote/', include('django_summernote.urls')),
    re_path(r'^2020/admin/', admin.site.urls),

    re_path(r'^2020/i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    re_path(r'^2020/?$', index, name='index'),
    re_path(r'^2020/accounts/', include('allauth.urls')),
    re_path(r'^2020/login/$', login, name='login'),
    re_path(r'^2020/logout/$', logout, name='logout'),
    re_path(r'^2020/announcement/', include('program.urls')),
    re_path(r'^2020/profile/', include('user.urls')),
    re_path(r'^2020/coc/$', RedirectView.as_view(url="/2020/about/coc", permanent=False)),
    re_path(r'^2020/slack/$', SlackInvitation.as_view(), name='slack-invitation'),

    # YouTube redirect
    re_path(r'^2020/(?P<day>\w{3})/(?P<room>\d{3})/$', ProgramRedirect.as_view()),
    re_path(r'^2020/(lt|LT)/(?P<day>\w{3})/$', LightningTalkRedirect.as_view()),
    re_path(r'^2020/closing/$', ClosingRedirect.as_view()),

    re_path(r'^2020/sponsor/', include('sponsor.urls')),
    re_path(r'^2020/program/', include('program.urls')),
    re_path(r'^2020/registration/', include('registration.urls')),

    re_path(r'^2020/about/patron/$', PatronList.as_view(), name='patrons'),
    re_path(r'^2020/about/organizing-team/$', StaffList.as_view(), name='staffs'),

    re_path(r'^2020/subscribe/$', NewsLetterAdd.as_view(), name='subscribe'),
    re_path(r'^2020/unsubscribe/$', NewsLetterRemove.as_view(), name='unsubscribe'),
    re_path(r'^2020/unsubscribe/(?P<mail>[\w\.@]+)$', NewsLetterRemoveConfirm.as_view(), name='unsubscribe-confirm'),

    # for rosetta
    re_path(r'^2020/rosetta/', include('rosetta.urls')),

    # cfp (contribution의 하위 url에 두기위해 별도로 기술)
    re_path(r'^2020/contribution/about/$', ContributionHome.as_view()),
    re_path(r'^2020/contribution/review-talk-proposal/$',
            login_required(OpenReviewHome.as_view()), name='openreview'),
    re_path(r'^2020/contribution/review-talk-proposal/set/$',
            login_required(OpenReviewList.as_view()), name='openreview-list'),
    re_path(r'^2020/contribution/review-talk-proposal/review/(?P<pk>\d+)$',
            login_required(OpenReviewUpdate.as_view()), name='openreview-update'),
    re_path(r'^2020/contribution/review-talk-proposal/review/result/$',
            login_required(OpenReviewResult.as_view()), name='openreview-result'),
    re_path(r'^2020/contribution/lightning-talk/home/$',
            login_required(LightningTalkHome.as_view()), name='lightning-talk'),
    re_path(r'^2020/contribution/lightning-talk/propose/$',
            login_required(LightningTalkCreate.as_view()), name='lightning-talk-propose'),
    re_path(r'^2020/contribution/lightning-talk/detail/$',
            login_required(LightningTalkDetail.as_view()), name='lightning-talk-detail'),
    re_path(r'^2020/contribution/lightning-talk/edit/(?P<pk>\d+)$',
            login_required(LightningTalkUpdate.as_view()), name='lightning-talk-edit'),

    # for flatpages
    re_path(r'^(?P<url>.*/)$', views.flatpage, name='flatpage'),

    prefix_default_language=False
)

handler404 = 'pyconkr.views.error_page_404'
handler500 = 'pyconkr.views.error_page_500'

# for development
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
