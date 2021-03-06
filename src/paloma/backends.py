# -*- coding: utf-8 -*-
''' Django Backend Implementation
    - https://docs.djangoproject.com/en/dev/topics/email/
'''
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.backends.smtp import EmailBackend as DjangoEmailBackend
from django.core.mail.message import sanitize_address
from email.utils import parseaddr

from paloma.tasks import send_email,bounce

from django.conf import settings

class PalomaEmailBackend(BaseEmailBackend):
    ''' A Django Email Backend to send emails thru Celery Task queue.
    ''' 
    def send_messages(self, email_messages, **kwargs):
        ''' Django Email Backend API - send_messages

            :param email_messages: list of django.core.mail.messages.EmailMessage instance

            - This implementation delegates STMP task to Celery worker.
        '''
        results = []
        for msg in email_messages:
            results.append(send_email.delay(msg, **kwargs)) #:asynchronous send_email 
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

class SmtpEmailBackend(DjangoEmailBackend):
    ''' handling SMTP 
    '''
    def _send(self, email_message):
        """A helper method that does the actual sending.

            :param email_message: EmaiMesage instance
            :type  email_message: django.core.mail.message.EmailMessage
        """

        if not email_message.recipients():
            return False

        #:Extended parameters for SMTP
        extended = getattr(email_message,"extended",{} )
         
        from_email = sanitize_address(
                extended.get('return_path',None) or email_message.from_email
                , email_message.encoding)
        recipients = [sanitize_address(addr, email_message.encoding)
                      for addr in email_message.recipients()]

        #: Python standard email.message.Message
        mailobj = email_message.message()
    
        #: message_id ->Message-ID
        if extended.has_key('message_id'):
            if mailobj.has_key('Message-ID'):
                mailobj.replace_header('Message-ID',extended['message_id'])
            else:
                mailobj.add_header('Message-ID',extended['message_id'])

        try:
            #: connection: smtplib.SMTP
            self.connection.sendmail(
                    from_email, recipients,mailobj.as_string() )
        except:
            if not self.fail_silently:
                raise
            return False
        return True
