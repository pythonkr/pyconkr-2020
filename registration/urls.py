from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import re_path, path

from . import views

urlpatterns = [
    path('ticket', views.TicketList.as_view(), name='ticket'),
    path('ticket/buy', login_required(views.RegistrationHome.as_view()), name='registration_index'),
]
