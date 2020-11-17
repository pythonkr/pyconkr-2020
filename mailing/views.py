from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView, TemplateView
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.db.models import ObjectDoesNotExist

from registration.models import Ticket
from .forms import NewsLetterAddForm, SlackAddForm
from .models import NewsLetter
from program.slack import slack_invitation_request
from pyconkr.views import get_KST_now

import constance


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
    template_name = 'slack_invitation_add.html'

    def get(self, request, *args, **kwargs):
        KST, now = get_KST_now()
        if not (constance.config.SLACK_INVITATION_OPEN < now < constance.config.SLACK_INVITATION_CLOSE):
            context = {
                'title': _('초대 기간이 아닙니다.'),
                'base_content': _('참가자 슬랙 초대 기간이 아닙니다.')
            }
            return render(self.request, 'base.html', context=context)

    def get_initial(self):
        if self.request.user.is_authenticated:
            init_val = super().get_initial()
            init_val['email_address'] = self.request.user.email
            return init_val

    def form_valid(self, form):
        if form.instance.agree_coc is False:
            raise HttpResponseBadRequest

        if NewsLetter.objects.filter(email_address=form.instance.email_address).exists() \
                or Ticket.objects.filter(user__email=form.instance.email_address).exists():
            context = {
                'title': _('중복된 이메일입니다.'),
                'base_content': _(
                    '이미 초대 신청된 메일 주소입니다. '
                    '<a href="https://pyconkr2020.slack.com/" target="_blank">https://pyconkr2020.slack.com/</a> '
                    '으로 로그인해보세요!<br>'
                    '신청하신 적이 없다면 pyconkr@pycon.kr로 알려주세요.')
            }
            return render(self.request, 'base.html', context=context)
        else:
            form.save()

            slack_invitation_request(form.instance.email_address)

            context = {
                'title': _('신청이 완료되었습니다.'),
                'base_content': _('확인 후 메일드리겠습니다. 감사합니다.')
            }
            return render(self.request, 'base.html', context=context)
