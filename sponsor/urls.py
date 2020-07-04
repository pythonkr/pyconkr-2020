from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from sponsor.views import SponsorCreate, SponsorDetail, SponsorProposalHome, SponsorProposalDetail, SponsorUpdate, \
    VirtualBooth, VirtualBoothDetail, VirtualBoothUpdate


from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    path('join/home/',
         SponsorProposalHome.as_view(), name='sponsor_propose_home'),
    path('join/form/',
         login_required(SponsorCreate.as_view()), name='sponsor_propose'),
    path('join/detail/',
         SponsorProposalDetail.as_view(), name='sponsor_proposal_detail'),
    path('join/edit/',
         SponsorUpdate.as_view(), name='sponsor_proposal_edit'),
    re_path(r'^detail/(?P<slug>\w+)/$',
            SponsorDetail.as_view(), name='sponsor_detail'),
    path('virtual_booth/',
         VirtualBooth.as_view(), name='virtual_booth_home'),
    re_path(r'^virtual_booth/(?P<slug>\w+)/$',
            VirtualBoothDetail.as_view(), name='virtual_booth'),
    re_path(r'^virtual_booth/(?P<slug>\w+)/edit/',
            VirtualBoothUpdate.as_view(), name='virtual_booth_update'),
]
