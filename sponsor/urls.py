from django.urls import path
from sponsor.views import SponsorList, SponsorDetail, SponsorCreate


from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    path('list/',
         SponsorList.as_view(), name='sponsors'),
    path('detail/<slug:slug>/',
         SponsorDetail.as_view(), name='sponsor'),
    path('join/',
         SponsorCreate.as_view(), name='join_sponsor'),
]
