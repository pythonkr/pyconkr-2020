from django.db import models
from jsonfield import JSONField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.urls import reverse
import constance
import datetime

User = get_user_model()


class ProgramCategory(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Proposal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    brief = models.TextField(max_length=1000)
    desc = models.TextField(max_length=4000)
    comment = models.TextField(max_length=4000, null=True, blank=True)

    difficulty = models.CharField(max_length=1,
                                  choices=(
                                      ('B', _('Beginner')),
                                      ('I', _('Intermediate')),
                                      ('E', _('Experienced')),
                                  ))

    duration = models.CharField(max_length=1,
                                choices=(
                                    ('S', _('25min')),
                                    ('L', _('40min')),
                                ))

    language = models.CharField(max_length=1,
                                choices=(
                                    ('', '---------'),
                                    ('K', _('Korean')),
                                    ('E', _('English')),
                                ),
                                default='')

    category = models.ForeignKey(
        ProgramCategory, on_delete=models.SET_DEFAULT, null=True, blank=True, default=14)
    accepted = models.BooleanField(default=False)
    introduction = models.TextField(max_length=1000, null=True, blank=True, help_text=_('발표 소개 페이지에 들어가는 내용입니다.'))
    video_url = models.CharField(max_length=255, null=True, blank=True, help_text=_('발표 영상 URL'))
    slide_url = models.CharField(max_length=255, null=True, blank=True, help_text=_('발표 자료 URL'))
    video_open_at = models.DateTimeField(null=True, blank=True, help_text=_('파이콘 한국 유튜브에 공개되는 시간'))

    def __str__(self):
        return self.title


class OpenReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)
    comment = models.TextField(max_length=2000)
    category = models.ForeignKey(ProgramCategory, on_delete=models.CASCADE, null=True, blank=True)
    submitted = models.BooleanField(default=False)

    @property
    def has_comment(self):
        return len(self.comment) > 0

    def __str__(self):
        return self.proposal.title


class LightningTalk(models.Model):
    class Meta:
        ordering = ['created_at', ]

    title = models.CharField(max_length=255, null=True, help_text='라이트닝 토크 제목')
    owner = models.OneToOneField(User, blank=True, null=True, on_delete=models.SET_NULL)
    slide_url = models.CharField(max_length=511, null=True)
    day = models.IntegerField(choices=(
        (1, _('토요일')),
        (2, _('일요일')),
    ))
    comment = models.TextField(blank=True, default='')

    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Sprint(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, help_text=_('스프린트를 등록한 유저'))
    title = models.CharField(max_length=255, help_text=_('스프린트 제목'))
    desc = models.TextField(max_length=4000, help_text=_('스프린트 설명'), null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True,
                           help_text=_('홈페이지에 공개되는 스프린트 관련 주소입니다.'))
