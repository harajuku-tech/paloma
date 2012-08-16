# -*- coding: utf-8 -*-

from paloma.management.commands import GenericCommand
from paloma.mails import send_mail_simple,send_mail_from_file
from paloma.tasks import trigger_schedule

from django.utils import timezone, dateparse
from celery import app

from optparse import make_option
from datetime import datetime
import commands
import os

class Command(GenericCommand):
    ''' Celery Utility
    '''
    args = ''
    help = ''

    option_list = GenericCommand.option_list + (
        )
    ''' Command Option '''


    def handle_revoke(self,*args,**options):
        ''' revoke specified task
        '''
        if len(args) == 2:
            print "Revoking task ",args[1]
            app.current_app().control.revoke(args[1]) 
