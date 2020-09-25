import datetime
import time

from django.contrib.auth import get_user_model
from django.core.mail import send_mail, send_mass_mail, EmailMessage, EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from mailing.models import Mailing, NewsLetter
from user.models import Profile
from registration.models import Ticket


@receiver(post_save, sender=Mailing)
def send_email_immediately(sender, instance, created, **kwargs):
    KST = datetime.timezone(datetime.timedelta(hours=9))
    now = datetime.datetime.now(tz=KST)

    user_model = get_user_model()

    send_to_participants = instance.send_to
    send_to_subscriber = instance.send_to_newsletter_subscriber

    if created is True:
        send_list = list()

        if send_to_participants == 'INFO':
            send_list = [m.user.email for m in Ticket.objects.all()]
        elif send_to_participants == 'AD':
            send_list = [m.user.email for m in Ticket.objects.filter(user__profile__agreement_receive_advertising_info=True)]

        if send_to_subscriber == 'YES':
            subscriber_list = [m.email_address for m in NewsLetter.objects.all()]
            send_list = send_list + subscriber_list

        email = EmailMultiAlternatives(
            instance.title,
            instance.content,
            instance.sender_name,
            ['pyconkr@pycon.kr'],  # To
            send_list,  # bcc
        )

        email.attach_alternative(instance.content, "text/html")
        email.content_subtype = 'html'
        email.mixed_subtype = 'related'

        email.send(fail_silently=False)

        instance.send_successfully = True
        instance.save()
