from django.contrib.auth.decorators import login_required
from django.urls import re_path
from user.views import ProfileDetail, ProfileUpdate

from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    re_path(r'^$',
            login_required(ProfileDetail.as_view()), name='profile'),
    re_path(r'^edit/$',
            login_required(ProfileUpdate.as_view()), name='profile_edit'),
]
