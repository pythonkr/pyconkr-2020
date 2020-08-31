from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView, TemplateView
from django.urls import reverse
from django.db.models import ObjectDoesNotExist

from .forms import NewsLetterAddForm
from .models import NewsLetter


class NewsLetterAdd(CreateView):
    form_class = NewsLetterAddForm
    template_name = "newsletter_add.html"

    def get(self, request, *args, **kwargs):
        return super(NewsLetterAdd, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        if NewsLetter.objects.filter(email_address=form.instance.email_address).exists():
            return redirect("/2020/subscribe/fail/")
        else:
            form.save()
            return redirect("/2020/subscribe/success/")


class NewsLetterRemove(CreateView):
    model = NewsLetter
    form_class = NewsLetterAddForm
    template_name = "newsletter_remove.html"

    def form_valid(self, form):
        if NewsLetter.objects.filter(email_address=form.instance.email_address).exists():
            return HttpResponseRedirect(reverse('unsubscribe-confirm', kwargs={'mail': form.instance.email_address}))
        else:
            return redirect("/2020/unsubscribe/fail/")


class NewsLetterRemoveConfirm(DeleteView):
    model = NewsLetter
    template_name = "newsletter_remove_confirm.html"
    success_url = "/2020/unsubscribe/success/"

    def get_object(self, queryset=None):
        if NewsLetter.objects.filter(email_address=self.kwargs['mail']).exists():
            queryset = NewsLetter.objects.filter(email_address=self.kwargs['mail'])
        elif queryset is None:
            raise Http404

    def delete(self, request, *args, **kwargs):
        delete_address = NewsLetter.objects.get(email_address=self.kwargs['mail'])
        delete_address.delete()

        return redirect("/2020/unsubscribe/success/")
