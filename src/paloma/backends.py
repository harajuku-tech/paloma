from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

from paloma.tasks import send_email

class CeleryEmailBackend(BaseEmailBackend):

    def send_messages(self, email_messages, **kwargs):
        results = []
        for msg in email_messages:
            results.append(send_email.delay(msg, **kwargs))
        return results
