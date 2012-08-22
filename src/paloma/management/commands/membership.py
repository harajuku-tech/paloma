# -*- coding: utf-8 -*-

from paloma.management.commands import GenericCommand
from paloma.mails import send_mail_simple,send_mail_from_file
from paloma.tasks import trigger_schedule

from django.utils import timezone, dateparse

from optparse import make_option
from datetime import datetime
import commands
import os

class Command(GenericCommand):
    ''' paloma membership management
    '''
    args = ''
    help = ''

    option_list = GenericCommand.option_list + (
        make_option('--username',
            action='store',
            dest='username',
            default=None,
            help=u"Django User's username"),

        )
    ''' Command Option '''

    def handle_withdraw(self,*args,**options):
        '''　withdraw 

        .. todo::
            - backup user's data as JSON fixture 
        '''
        print "withdraw user ",options
        if options.get('username',"") != "":
            from django.contrib.auth.models import User
            user = User.objects.get(username=options['username'])
            user.mailbox_set.all().delete()
            user.delete()
