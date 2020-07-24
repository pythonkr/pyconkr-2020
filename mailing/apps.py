from django.apps import AppConfig


class MailingConfig(AppConfig):
    name = 'mailing'

    def ready(self):
        import mailing.signal
