from django.contrib.auth.decorators import login_required
from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^ticket/$', views.TicketList.as_view(), name='ticket'),
    re_path(r'^ticket/buy/$', login_required(views.RegistrationHome.as_view()), name='registration_index'),
]
