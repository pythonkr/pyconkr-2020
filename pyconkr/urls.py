from django.conf.urls.i18n import i18n_patterns
from django.urls import re_path, include

urlpatterns = i18n_patterns(
    re_path(r'^registration/', include('registration.urls')),
    re_path(r'^2020/', include('web2020.urls')),
    re_path(r'^2018/', include('web2018.urls')),

    # # for flatpages
    # re_path(r'^pages/', include('django.contrib.flatpages.urls')),
    # re_path(r'^(?P<url>.*/)$', views.flatpage, name='flatpage'),

    prefix_default_language=False
)
