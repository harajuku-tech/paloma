# -*- coding: utf-8 -*-

from paloma.management.commands import GenericCommand
#from django.core.management.base import BaseCommand, CommandError

from optparse import make_option
from datetime import datetime
import commands
import os

class Command(GenericCommand):
    ''' paloma maile management
    '''
    args = ''
    help = ''

    option_list = GenericCommand.option_list + (

        )
    ''' Command Option '''

    def handle_send(self,*args,**options):
        '''　send

        '''
        import sys
        from email import message_from_file
        fp = sys.stdin if options['file'] == 'stdin' else open(options['file'])
        msg = message_from_file(fp)

        from django.core.mail import send_mail
        send_mail(msg['Subject'],str(msg),msg['From'],msg['To'].split(',') )

    def handle_help(self,*args,**options):
        '''  help
        '''
        import re
        for i in dir(self):
            m = re.search('^handle_(.*)$',i)
            if m == None:
                continue
            print m.group(1)
