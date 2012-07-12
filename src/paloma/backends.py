from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

from paloma.tasks import send_email

from django.conf import settings

class CeleryEmailBackend(BaseEmailBackend):

    def send_messages(self, email_messages, **kwargs):
        results = []
        for msg in email_messages:
            if getattr(settings,"BOUNCE_HANDLER_ASYNC",True):
                results.append(send_email.delay(msg, **kwargs))
            else:
                results.append(send_email(msg, **kwargs))
        return results
