# -*- coding: utf-8 -*-
''' Django Backend Implementation
    - https://docs.djangoproject.com/en/dev/topics/email/
'''
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from email.utils import parseaddr

from paloma.tasks import send_email,bounce

from django.conf import settings

class CeleryEmailBackend(BaseEmailBackend):
    ''' A Django Email Backend to send emails thru Celery Task queue.
    ''' 

    def send_messages(self, email_messages, **kwargs):
        ''' Django Email Backend API - send_messages

            :param email_messages: list of django.core.mail.messages.EmailMessage instance

            - This implementation delegates STMP task to Celery worker.
        '''
        results = []
        for msg in email_messages:
            results.append(send_email.delay(msg, **kwargs))
        return results

class JournalEmailBackend(BaseEmailBackend):
    ''' A Django Email Backend to save email 
        directly  to :ref:`paloma.models.Journal` model
    ''' 

    def send_messages(self, email_messages, **kwargs):
        ''' Django Email Backend API - send_messages

            :param email_messages: list of django.core.mail.messages.EmailMessage instance

            - https://github.com/django/django/blob/master/django/core/mail/message.py 

        .. todo::
            - DO ERROR CHECK!!!! 
            - DO ERROR TRACE!!!!
        ''' 
        try:
            sender  = parseaddr( email_messages[0].from_email )[1]
            recipient =parseaddr( email_messages[0].to[0] )[1] 
            bounce(sender,recipient,email_messages[0].message().as_string(),True )
            return 1
        except Exception,e:
            return 0
