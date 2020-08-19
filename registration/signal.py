from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save)
def send_ticket_info(sender, **kwargs):
    print("sender: ", sender)
    print("kwargs: ", kwargs)
    
    # TODO: 티켓 메일발송
