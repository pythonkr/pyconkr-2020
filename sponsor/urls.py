from django.urls import path
from sponsor.views import SponsorList, SponsorDetail, SponsorUpdate


from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    path('list/',
         SponsorList.as_view(), name='sponsors'),
    path('detail/<int:pk>/',
         SponsorDetail.as_view(), name='sponsor'),
    path('join/',
         SponsorUpdate.as_view(), name='join_sponsor'),
]
