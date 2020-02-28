# -*- coding: utf-8 -*-
from datetime import datetime
from uuid import uuid4

from constance import config
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.urls import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import date as _date
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail import ImageField as SorlImageField


class EmailToken(models.Model):
    email = models.EmailField(max_length=255)
    token = models.CharField(max_length=64, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.token = str(uuid4())
        super(EmailToken, self).save(*args, **kwargs)


class Banner(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=255, null=True, blank=True)
    image = SorlImageField(upload_to='banner')
    desc = models.TextField(null=True, blank=True)

    begin = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
