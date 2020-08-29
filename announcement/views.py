from datetime import datetime

from django.db.models import Q
from django.views.generic import ListView, DetailView

from .models import Announcement


class AnnouncementList(ListView):
    model = Announcement

    def get_queryset(self):
        queryset = super(AnnouncementList, self).get_queryset()
        return queryset.filter(Q(announce_after__isnull=True) | Q(announce_after__lt=datetime.now()))


class AnnouncementDetail(DetailView):
    model = Announcement
