from django.db import models
from jsonfield import JSONField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from registration.models import Option
from django.urls import reverse
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


class Room(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('room', args=[self.id])

    def __str__(self):
        return self.name


class Speaker(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=100, db_index=True)
    organization = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=255, db_index=True,
                              null=True, blank=True)
    image = models.ImageField(upload_to='speaker', null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    info = JSONField(blank=True, help_text=_('help-text-for-speaker-info'))

    class Meta:
        ordering = ['name']

    def get_badges(self, size_class=""):
        badge = \
            '<a class="btn btn-social btn-social-default {} btn-{}" href="{}" target="_blank">' \
            '<i class="fa fa-external-link fa-{}"></i>{}</a>'
        fa_replacement = {
            "homepage": "home",
            "blog": "pencil",
        }
        result = []
        if type(self.info) == str:
            return '<div class="badges">{}</div>'.format(' '.join(result))

        for site, url in self.info.items():
            result.append(badge.format(
                size_class,
                site, url,
                fa_replacement.get(site, site), site.capitalize()
            ))
        return '<div class="badges">{}</div>'.format(' '.join(result))

    def get_badges_xs(self):
        return self.get_badges("btn-xs")

    def get_absolute_url(self):
        return reverse('speaker', args=[self.slug])

    def get_image_url(self):
        if self.image:
            return self.image.url

        return static('image/anonymous.png')

    def __str__(self):
        return '%s / %s' % (self.name, self.slug)


class Program(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    brief = models.TextField(null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    slide_url = models.CharField(max_length=255, null=True, blank=True)
    pdf_url = models.CharField(max_length=255, null=True, blank=True)
    video_url = models.CharField(max_length=255, null=True, blank=True)
    speakers = models.ManyToManyField(Speaker, blank=True)
    difficulty = models.CharField(max_length=1,
                                  choices=(
                                      ('B', _('Beginner')),
                                      ('I', _('Intermediate')),
                                      ('E', _('Experienced')),
                                  ), default='B')

    duration = models.CharField(max_length=1,
                                choices=(
                                    ('S', _('25min')),
                                    ('L', _('40min')),
                                ), default='S')

    language = models.CharField(max_length=1,
                                choices=(
                                    ('E', _('English')),
                                    ('K', _('Korean')),
                                ), default='E')

    date = models.ForeignKey(
        ProgramDate, on_delete=models.SET_NULL, null=True, blank=True)
    rooms = models.ManyToManyField(Room, blank=True)
    times = models.ManyToManyField(ProgramTime, blank=True)
    category = models.ForeignKey(
        ProgramCategory, on_delete=models.SET_NULL, null=True, blank=True)

    is_recordable = models.BooleanField(default=True)
    is_breaktime = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('program', args=[self.id])

    def room(self):
        rooms = self.rooms.all()

        if rooms.count() == Room.objects.all().count():
            return ''

        return ', '.join([_.name for _ in self.rooms.all()])

    def get_sort_times(self):
        return self.times.order_by('begin', 'id')

    def get_slide_url_by_begin_time(self):
        from datetime import datetime

        if not config.SHOW_SLIDE_DATA:
            return None

        time = self.get_sort_times().first()

        if not time:
            return None

        opendate = datetime(year=time.day.day.year, month=time.day.day.month, day=time.day.day.day,
                            hour=time.begin.hour,
                            minute=time.begin.minute)
        if datetime.now() >= opendate:
            return self.slide_url
        else:
            return None

    def begin_time(self):
        return self.get_sort_times().first().begin.strftime("%H:%M")

    def get_speakers(self):
        return ', '.join([u'{}({})'.format(_.name, _.email) for _ in self.speakers.all()])

    get_speakers.short_description = u'Speakers'

    def get_times(self):
        times = self.get_sort_times()

        if times:
            return '%s - %s' % (times.first().begin.strftime("%H:%M"),
                                times[len(times) - 1].end.strftime("%H:%M"))
        else:
            return _("Not arranged yet")

    def __str__(self):
        return self.name


class Preference(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('user', 'program')


class Proposal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

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

    category = models.CharField(max_length=25,
                                choices=(
                                    ('', '---------'),
                                    ('PL', _('Python Library')),
                                    ('DM', _('Development Method with Python')),
                                    ('DA', _('Data Analytics')),
                                    ('LS', _('Life / Social')),
                                    ('CV', _('Computer Vision')),
                                    ('RE', _('Robotics / Embedded System')),
                                    ('DG', _('Data Gathering')),
                                    ('BC', _('Blockchain')),
                                    ('PC', _('Python Community')),
                                    ('WS', _('Web Service')),
                                    ('DL', _('Deep Learning & AI')),
                                    ('PF', _('Python Core & Fundamental')),
                                    ('DS', _('Data Science')),
                                    ('etc', _('etc')),
                                ),
                                default='', null=True, blank=True)

    def __str__(self):
        return self.title


class TutorialProposal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    brief = models.TextField(max_length=1000)
    desc = models.TextField()
    comment = models.TextField(max_length=4000, null=True, blank=True)

    difficulty = models.CharField(max_length=1,
                                  choices=(
                                      ('B', _('Beginner')),
                                      ('I', _('Intermediate')),
                                      ('E', _('Experienced')),
                                  ))

    duration = models.CharField(max_length=1,
                                choices=(
                                    ('S', _('1 hour')),
                                    ('M', _('2 hours')),
                                    ('L', _('4 hours')),
                                ))

    language = models.CharField(max_length=1,
                                choices=(
                                    ('E', _('English')),
                                    ('K', _('Korean')),
                                ),
                                default='E')

    capacity = models.IntegerField(null=False)
    confirmed = models.BooleanField(default=False)
    option = models.ForeignKey(Option, default=None, on_delete=models.SET_NULL,
                               null=True, blank=True, verbose_name="구매 티켓 종류")
    begin_date = models.DateField(null=True, blank=True)
    begin_time = models.TimeField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tutorial', args=[self.id])

    @property
    def begin_at(self):
        if not self.begin_date or not self.begin_time:
            return None
        return datetime.combine(self.begin_date, self.begin_time)

    @property
    def end_at(self):
        if not self.end_date or not self.end_time:
            return None
        return datetime.combine(self.end_date, self.end_time)


class SprintProposal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    project_url = models.CharField(max_length=1024)
    project_brief = models.TextField(max_length=1000)
    contribution_desc = models.TextField()
    comment = models.TextField(max_length=4000, null=True, blank=True)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('sprint', args=[self.id])


class TutorialCheckin(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tutorial = models.ForeignKey(
        TutorialProposal, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('user', 'tutorial')


class SprintCheckin(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    sprint = models.ForeignKey(
        SprintProposal, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('user', 'sprint')
