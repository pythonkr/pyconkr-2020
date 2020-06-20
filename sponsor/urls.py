from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from sponsor.views import SponsorList, SponsorProposal, SponsorDetail, SponsorUpdate, VirtualBooth, VirtualBoothDetail


from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    path('list/',
         SponsorList.as_view(), name='sponsors'),
    re_path(r'^detail/(?P<slug>\w+)/$',
            SponsorDetail.as_view(), name='sponsor_detail'),
    re_path('join/',
            login_required(SponsorProposal.as_view()), name='sponsor_propose'),
    # 최초생성 및 갱신
    path('update/',
         SponsorUpdate.as_view(), name='join_sponsor'),
    path('virtual_booth/',
         VirtualBooth.as_view(), name='virtual_booth_home'),
    re_path(r'^virtual_booth/(?P<slug>\w+)/$',
            VirtualBoothDetail.as_view(), name='virtual_booth')
]
