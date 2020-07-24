import datetime

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from mailing.models import Mailing
from user.models import Profile


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
            send_list = [(m.email, m.username) for m in user_model.objects.all()]
        elif send_to_participants == 'AD':
            send_list = [(m.user.email, m.user.username) for m in
                         Profile.objects.filter(agreement_receive_advertising_info=True)]

        # TODO 뉴스레터
        if send_to_subscriber == 'YES':
            subscriber_list = []
            send_list = send_list + subscriber_list

#        print('전송 목록:', send_list)

        for email_info in send_list:
            send_mail(
                instance.title,          # 제목
                instance.content,        # 내용
                instance.sender_name,    # 보내는 이메일  (settings에 설정해서 작성안해도 됨)
                [email_info[0]],                    # 받는 이메일 리스트
                fail_silently=False,
                html_message=instance.content
            )

        instance.send_successfully = True
        instance.save()
        print('메일전송완료')
