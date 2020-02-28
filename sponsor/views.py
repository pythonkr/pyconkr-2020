from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sponsor


class SponsorList(ListView):
    model = Sponsor


class SponsorDetail(DetailView):
    model = Sponsor
