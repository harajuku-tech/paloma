"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
#
from django.conf import settings
from django.core import mail
#
from djcelery_email.tasks import send_email

class ScheduleTests(TestCase):

    fixtures=['auth','paloma','foods']

    def test_simple(self):
        ''' python manage.py test foods.ScheduleTests.test_simple
        '''
        from paloma.models import Schedule,Message
        for m in Schedule.objects.all():
            print m.text 
            m.generate_messages()

        for m in Message.objects.all():
            print m.text 

class DjangoCeleryEmailTests(TestCase):

    def test_sending_email(self):
        import settings
        print "test_sending_email",settings.EMAIL_BACKEND
        
        
        from django.core.mail import send_mail
        send_mail('test', 'Testing with Celery! w00t!!', 'gmail@hoge.com', ['hdknr@hoge.deb'])
        
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'test')

#    def test_sending_mass_email(self):
#        emails = (
#            ('mass 1', 'mass message 1', 'gmail@hoge.com', ['hdknr@hoge.deb']),
#            ('mass 2', 'mass message 2', 'gmail@hoge.com', ['hdknr@hoge.sqg']),
#        )
#        results = mail.send_mass_mail(emails)
#        self.assertEqual(len(mail.outbox), 2)
#        self.assertEqual(len(results), 2)
#        self.assertEqual(mail.outbox[0].subject, 'mass 1')
#        self.assertEqual(mail.outbox[1].subject, 'mass 2')
    
    def test_setting_extra_configs(self):
        self.assertEqual(send_email.queue, 'django_email')
        self.assertEqual(send_email.delivery_mode, 1)
        self.assertEqual(send_email.rate_limit, '50/m')
