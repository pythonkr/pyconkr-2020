from collections import OrderedDict

from django.utils import timezone
from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from pyconkr.models import Banner
from sponsor.models import SponsorLevel, Sponsor


def default(request):
    title = None
    # remove i18n_patterns prefix for flatpage
    url = request.path.replace('/' + request.LANGUAGE_CODE, '')
    if settings.FORCE_SCRIPT_NAME:
        url = url[len(settings.FORCE_SCRIPT_NAME):]
    base_content = FlatPage.objects.filter(url=url).first()
    paid_sponsor = Sponsor.objects.filter(accepted=True, paid_at__isnull=False).exclude(logo_image="").exclude(
        level__order=0)
    paid_levels = []
    for sponsor in paid_sponsor:
        paid_levels.append(sponsor.level)

    submenu = None
    menu = OrderedDict([
        (
            'about', {
                'title': _('About'),
                'submenu': OrderedDict([
                    ('pyconkr', {'title': _('About PyCon Korea 2020')}),
                    ('schedule', {'title': _('Important Dates')}),
                    ('patron', {'title': _('Patrons')}),
                    ('coc', {'title': _('Code of Conduct')}),
                    ('organizing-team', {'title': _('Organizing Team')}),
                    ('previous-pyconkr', {'title': _('Previous PyCon Korea')}),
                ])
            }
        ),
        (
            'program', {
                'title': _('Program'),
                'submenu': OrderedDict([
                    ('keynote', {'title': _('Keynotes')}),
                    ('talks', {'title': _('Talks')}),
                    ('talk-schedule', {'title': _('Talks Schedule')}),
                    ('lightning-talk', {'title': _('Lightning Talk')}),
                    ('sprint', {'title': _('Sprint')}),
                ])
            }
        ),
        (
            'contribution', {
                'title': _('Contribution'),
                'submenu': OrderedDict([
                    ('about', {'title': _('About Contribution')}),
                    ('cfp/guide', {'title': _('How to Submit a Proposal')}),
                    ('cfp', {'title': _('Proposing a Talk')}),
                    ('review-talk-proposal',
                     {'title': _('Review Talk Proposal')}),
                    ('lightning-talk/home',
                     {'title': _('Proposing a Lightning Talk')}),
                    ('recommending-keynote',
                     {'title': _('Recommending Keynote')}),
                    ('video-subtitle', {'title': _('Video Subtitle')}),
                ])
            }
        ),
        (
            'sponsor', {
                'title': _('Sponsor'),
                'submenu': OrderedDict([
                    ('prospectus', {'title': _('Prospectus')}),
                    ('benefit', {'title': _('Benefit')}),
                    ('join/home', {'title': _('Join as Sponsor')}),
                    ('faq', {'title': _('FAQ')}),
                    ('terms-of-sponsor', {'title': _('Terms of Sponsor')}),
                    ('virtual_booth', {'title': _('Virtual Booth')}),
                ])
            }
        ),
        (
            'registration', {
                'title': _('Registration'),
                'submenu': OrderedDict([
                    ('ticket', {'title': _('Buy Ticket')}),
                ])
            }
        )
    ])

    for k, v in menu.items():
        path = '/{}/'.format(k)

        if url.startswith(path):
            v['active'] = True
            title = v['title']

            if 'submenu' in v:
                submenu = v['submenu']

                for sk, sv in v['submenu'].items():
                    sv['path'] = '{}{}/'.format(path, sk)
                    subpath = sv['path']

                    if url == subpath:
                        sv['active'] = True
                        title = sv['title']

    now = timezone.now()
    banners = Banner.objects.filter(begin__lte=now, end__gte=now)

    c = {
        'menu': menu,
        'submenu': submenu,
        'banners': banners,
        'title': title,
        'domain': settings.DOMAIN,
        'base_content': base_content.content if base_content else '',
        'paid_levels': paid_levels,
    }
    return c


def sponsors(request):
    levels = SponsorLevel.objects.annotate(
        num_sponsors=Count('sponsor')).filter(num_sponsors__gt=0)

    return {
        'levels': levels,
    }
