from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Announcement


class AnnouncementList(ListView):
    model = Announcement

    def get_queryset(self):
        now = datetime.now()
        queryset = super(AnnouncementList, self).get_queryset()
        return queryset.filter(Q(announce_after__isnull=True) | Q(announce_after__lt=now))


class AnnouncementDetail(DetailView):
    model = Announcement
