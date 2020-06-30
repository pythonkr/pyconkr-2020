from django.conf import settings
from django.conf.urls import include, url, handler404, handler500
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib.flatpages import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from django.views.generic.base import TemplateView

from .views import index, robots
from .views import login, logout
from .views import PatronList

from program.views import ProposalCreate, OpenReviewUpdate
from program.views import OpenReviewList

from django.contrib import admin
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

    re_path(r'^2020/sponsor/', include('sponsor.urls')),
    re_path(r'^2020/program/', include('program.urls')),
    re_path(r'^2020/about/patron/$',
            PatronList.as_view(), name='patrons'),


    re_path(r'^2020/registration/', include('registration.urls')),

    # for rosetta
    re_path(r'^2020/rosetta/', include('rosetta.urls')),

    # cfp (contribution의 하위 url에 두기위해 별도로 기술)
    re_path(r'^2020/contribution/review-talk-proposal/$',
            login_required(OpenReviewList.as_view()), name='openreview-list'),
    re_path(r'^2020/contribution/review-talk-proposal/(?P<pk>\d+)$',
            login_required(OpenReviewUpdate.as_view()), name='openreview-update'),

    # for flatpages
    re_path(r'^(?P<url>.*/)$', views.flatpage, name='flatpage'),
    # re_path(r'^2020/pages/', include('django.contrib.flatpages.urls')),

    prefix_default_language=False
)

handler404 = 'pyconkr.views.error_page_404'
handler500 = 'pyconkr.views.error_page_500'

# for development
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
