import datetime
import os

from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from user.models import Profile


class Mailing(models.Model):
    CHOICE_SEND_TO_ALL_PARTICIPANT = [
        ('INFO', '정보성 메일'),
        ('AD', '광고성 메일'),
        ('NONE', '참가자에게 보내지 않음'),
    ]

    CHOICE_SEND_TO_SUBSCRIBER = [
        ('YES', '구독자에게 보내기'),
        ('NO', '구독자에게 보내지 않기')
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    send_datetime = models.DateTimeField(default=datetime.datetime(2020, 8, 1))
    send_to = models.CharField(
        max_length=100,
        choices=CHOICE_SEND_TO_ALL_PARTICIPANT,
        default='INFO',
    )
    send_to_newsletter_subscriber = models.CharField(
        max_length=100,
        choices=CHOICE_SEND_TO_SUBSCRIBER,
        default='NO',
    )
    send_successfully = models.BooleanField(default=False)
    sender_name = models.CharField(max_length=100, default='PyCon Korea')


class NewsLetter(models.Model):
    email_address = models.EmailField(help_text=_('소식을 받을 이메일 주소'))
    agree_coc = models.BooleanField(default=False, help_text=_('참가자 슬랙 초대용 CoC 동의 여부'))

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        return super().save(force_insert, force_update, using, update_fields)
