from django.db import models
from jsonfield import JSONField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.urls import reverse
import constance

User = get_user_model()


class ProgramCategory(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProgramDate(models.Model):
    day = models.DateField()

    def __str__(self):
        return _date(self.day, "Y-m-d (D)")


class ProgramTime(models.Model):
    name = models.CharField(max_length=100)
    begin = models.TimeField()
    end = models.TimeField()
    day = models.ForeignKey(
        ProgramDate, on_delete=models.SET_NULL, null=True, blank=True)

    def __meta__(self):
        ordering = ['begin']

    def __str__(self):
        return '%s - %s / %s / %s' % (self.begin, self.end, self.name, self.day)


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
