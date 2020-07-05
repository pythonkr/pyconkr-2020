import datetime

from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from user.models import Profile


class Mailing(models.Model):
    title = models.TextField()
    content = models.TextField()
    send_now = models.BooleanField()
    send_datetime = models.DateTimeField()
    send_to_all_participant = models.BooleanField()
    send_to_newsletter_subscriber = models.BooleanField()
    send_yn = models.BooleanField(default=False)
    sender_name = models.CharField(max_length=100, default='PyCon Korea')


class NewsLetter(models.Model):
    email_address = models.EmailField()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        return super().save(force_insert, force_update, using, update_fields)


@receiver(post_save, sender=Mailing)
def send_email_immediately(sender, instance, created, **kwargs):
    print('sender: ', sender)
    print('instance: ', instance)
    print('created: ', created)

    KST = datetime.timezone(datetime.timedelta(hours=9))
    now = datetime.datetime.now(tz=KST)

    if created is True:
        send_list = [m for m in Profile.objects.filter()]

        send_mail(
            instance.title,  # 제목
            instance.content,  # 내용
            instance.sender_name,  # 보내는 이메일  (settings에 설정해서 작성안해도 됨)
            [''],  # 받는 이메일 리스트
            fail_silently=False,
        )
        print('메일전송완료')