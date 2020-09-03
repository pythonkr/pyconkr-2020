from django.urls import re_path
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from . import views

admin.autodiscover()

urlpatterns = [
    re_path(r'^join/home/$', views.SponsorProposalHome.as_view(), name='sponsor_propose_home'),
    re_path(r'^join/form/$', login_required(views.SponsorCreate.as_view()), name='sponsor_propose'),
    re_path(r'^join/detail/$', views.SponsorProposalDetail.as_view(), name='sponsor_proposal_detail'),
    re_path(r'^join/edit/$', views.SponsorUpdate.as_view(), name='sponsor_proposal_edit'),
    re_path(r'^detail/(?P<slug>\w+)$', views.SponsorDetail.as_view(), name='sponsor_detail'),
    re_path(r'^virtual_booth/$', views.VirtualBooth.as_view(), name='virtual_booth_home'),
    re_path(r'^virtual_booth/(?P<slug>\w+)$', views.VirtualBoothDetail.as_view(), name='virtual_booth'),
    re_path(r'^virtual_booth/(?P<slug>\w+)/edit/$', views.VirtualBoothUpdate.as_view(), name='virtual_booth_update'),
    re_path(r'^login/$', views.LoginForSponsor.as_view(), name='login_for_sponsor'),
]
