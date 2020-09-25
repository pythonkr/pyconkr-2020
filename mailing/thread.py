import threading
from django.core.mail import EmailMultiAlternatives

# ref: https://qkr0990.github.io/development/2016/10/27/django-asynchronous-mail-send.html
# TODO 다음에는 Celery로...


class EmailThread(threading.Thread):
    def __init__(self, subject, body, from_email, recipient_list, fail_silently, html, bcc):
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.html = html
        self.bcc = bcc
        threading.Thread.__init__(self)

    def run (self):
        msg = EmailMultiAlternatives(self.subject, self.body, self.from_email, self.recipient_list, self.bcc)
        if self.html:
            msg.attach_alternative(self.html, "text/html")
            msg.content_subtype = 'html'
            msg.mixed_subtype = 'related'

        msg.send(self.fail_silently)


def send_mail(subject, body, from_email, recipient_list, fail_silently, html, bcc, *args, **kwargs):
    EmailThread(subject, body, from_email, recipient_list, fail_silently, html, bcc).start()
