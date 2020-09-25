from django.db.models.signals import post_save
from django.dispatch import receiver

from mailing.helper import send_ticket
from user.models import Profile
from registration.models import Ticket


@receiver(post_save, sender=Ticket)
def send_ticket_info(sender, instance, created, **kwargs):
    # 최초 작성 시에만 메일 발송
    if created is True:
        print("sender: ", sender)
        print("instance: ", instance)
        print("kwargs: ", kwargs)

        user_profile = Profile.objects.get(user=instance.user)

        send_ticket(user_profile)
