import datetime
import os

from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from user.models import Profile


class Mailing(models.Model):
    CHOICE_SEND_TO_ALL_PARTICIPANT = [
        ('INFO', '정보성 메일'),
        ('AD', '광고성 메일'),
        ('NONE', '참가자에게 보내지 않음'),
    ]

    CHOICE_SEND_TO_SUBSCRIBER = [
        ('YES', '구독자에게 보내기'),
        ('NO', '구독자에게 보내지 않기')
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    send_datetime = models.DateTimeField(default=datetime.datetime.now())
    send_to = models.CharField(
        max_length=100,
        choices=CHOICE_SEND_TO_ALL_PARTICIPANT,
        default='INFO'
    )
    send_to_newsletter_subscriber = models.CharField(
        max_length=100,
        choices=CHOICE_SEND_TO_SUBSCRIBER,
        default='NO'
    )
    send_yn = models.BooleanField(default=False)
    sender_name = models.CharField(max_length=100, default='PyCon Korea')


class NewsLetter(models.Model):
    email_address = models.EmailField()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        return super().save(force_insert, force_update, using, update_fields)


@receiver(post_save, sender=Mailing)
def send_email_immediately(sender, instance, created, **kwargs):
    # print('sender: ', sender)
    # print('instance: ', instance)
    # print('created: ', created)

    KST = datetime.timezone(datetime.timedelta(hours=9))
    now = datetime.datetime.now(tz=KST)

    user_model = get_user_model()

    send_to_participants = instance.send_to
    send_to_subscriber = instance.send_to_newsletter_subscriber

    print('참가자 전송 Flag:', send_to_participants)
    print('구독자 전송 Flag:', send_to_subscriber)

    if created is True:
        send_list = list()

        if send_to_participants == 'INFO':
            pass
        elif send_to_participants == 'AD':
            send_list = [(m.email, m.profile) for m in
                         user_model.objects.filter(profile__agreement_receive_advertising_info=True)]

        # TODO 뉴스레터
        if send_to_subscriber == 'YES':
            subscriber_list = []
            send_list = send_list + subscriber_list

        # send_list = [os.getenv('TEST_EMAIL'), ]
        print('전송 목록:', send_list)

        # send_mail(
        #     instance.title,          # 제목
        #     instance.content,        # 내용
        #     instance.sender_name,    # 보내는 이메일  (settings에 설정해서 작성안해도 됨)
        #     # [''],                    # 받는 이메일 리스트
        #     send_list,
        #     fail_silently=False,
        #     html_message=instance.content
        # )
        print('메일전송완료')
