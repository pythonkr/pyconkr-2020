from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, TemplateView
from django.urls import reverse

from .forms import NewsLetterAddForm


class NewsLetterAdd(CreateView):
    form_class = NewsLetterAddForm
    template_name = "pyconkr/newsletter_add.html"

    def get(self, request, *args, **kwargs):
        return super(NewsLetterAdd, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('index')
