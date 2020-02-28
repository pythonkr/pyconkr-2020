from django.urls import re_path
from sponsor.views import SponsorList, SponsorDetail


from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    re_path(r'^$',
            SponsorList.as_view(), name='sponsors'),
    re_path(r'^(?P<slug>[\w|-]+)$',
            SponsorDetail.as_view(), name='sponsor'),
]
