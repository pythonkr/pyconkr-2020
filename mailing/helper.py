from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

from user.models import Profile


def send_ticket(orm_profile: Profile):
    title = 'PyCon KR 2020에 등록해주셔서 감사합니다.'
    html_content = render_to_string('email_ticket.html', {'profile': orm_profile})
    sender_name = 'PyCon Korea'

    email = EmailMultiAlternatives(
        title,
        html_content,
        'PyCon Korea',
        [orm_profile.user.email],
    )

    email.attach_alternative(html_content, "text/html")
    email.content_subtype = 'html'  # set the primary content to be text/html
    email.mixed_subtype = 'related'  # it is an important part that ensures embedding of an image

    email.send(fail_silently=False)
