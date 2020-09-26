from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView, TemplateView
from django.urls import reverse
from django.db.models import ObjectDoesNotExist

from .forms import NewsLetterAddForm, SlackAddForm
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


class SlackInvitation(CreateView):
    model = NewsLetter
    form_class = SlackAddForm
    template_name = ''

    def form_valid(self, form):
        if NewsLetter.objects.filter(email_address=form.instance.email_address).exists():
            context = {
                'title': '중복된 이메일입니다.',
                'base_content': '이미 초대신청 된 메일주소입니다. 신청하신적이 없다면 저희에게 알려주세요.'
            }
            return render(self.request, 'base.html')
        else:
            form.save()
            context = {
                'title': '등록에 성공했습니다.',
                'base_content': '확인 후 메일드리겠습니다.'
            }
            return render(self.request, 'base.html', context=context)
