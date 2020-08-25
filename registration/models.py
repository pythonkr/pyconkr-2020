# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Ticket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_patron = models.BooleanField(default=False)
    price = models.IntegerField(default=0)
    ticket_purchase_datetime = models.DateTimeField(auto_now_add=True)
