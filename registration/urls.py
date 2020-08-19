from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import re_path, path

from . import views

urlpatterns = [
    path('purchase/', views.index, name='registration_index'),
    re_path(r'^status/(\d*)/$', views.status, name='registration_status'),
    re_path(r'^list/(\d*)/$', views.registrations, name='registration_list'),
    re_path(r'^checkins/(\d*)/$', views.checkins, name='registration_checkins'),
    re_path(r'^payment/(\d*)/$', views.payment, name='registration_payment'),
    re_path(r'^payment/$', views.payment_process, name='registration_payment'),
    re_path(r'^payment/callback/$', views.payment_callback, name='registration_callback'),
    re_path(r'^receipt/$',
        login_required(views.RegistrationReceiptDetail.as_view()), name='registration_receipt'),
    re_path(r'^payment/manual/(\d+)/$', views.manual_registration, name='manual_registration'),
    re_path(r'^payment/manual/payment/$', views.manual_payment_process, name='manual_payment'),
    re_path(r'^certificates/$', login_required(views.certificates), name='certificates'),
    re_path(r'^certificates_tutorial/$', login_required(views.certificates_tutorial), name='certificates_tutorial'),
    re_path(r'^certificates_sprint/$', login_required(views.certificates_sprint), name='certificates_sprint'),
    re_path(r'^issue/$', views.issue, name='registration_issue'),
    re_path(r'^issue/submit/$', views.issue_submit, name='registration_issue_submit'),
    re_path(r'^issue/print/(?P<registration_id>\d+)/$', views.issue_print, name='registration_issue_print'),
    re_path(r'^sprint/$', views.sprint, name='sprint_checkin'),
    re_path(r'^sprint/print/(?P<checkin_id>\d+)/$', views.sprint_print, name='sprint_checkin_print'),
]
