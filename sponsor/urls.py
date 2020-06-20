from django.urls import path, re_path
from sponsor.views import SponsorList, SponsorDetail, SponsorUpdate, VirtualBooth, VirtualBoothDetail


from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    path('list/',
         SponsorList.as_view(), name='sponsors'),
    re_path(r'^detail/(?P<slug>\w+)/$',
            SponsorDetail.as_view(), name='sponsor'),
    path('join/',
         SponsorUpdate.as_view(), name='join_sponsor'),
    path('virtual_booth/',
         VirtualBooth.as_view(), name='virtual_booth_home'),
    re_path(r'^virtual_booth/(?P<slug>\w+)/$',
            VirtualBoothDetail.as_view(), name='virtual_booth')
]
