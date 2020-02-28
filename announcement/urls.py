from django.urls import re_path
from .views import AnnouncementList, AnnouncementDetail

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    re_path(r'^$',
            AnnouncementList.as_view(), name='announcements'),
    re_path(r'^(?P<pk>\d+)$',
            AnnouncementDetail.as_view(), name='announcement'),
]
