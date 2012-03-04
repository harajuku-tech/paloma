# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from optparse import make_option
from datetime import datetime
import commands
import os

class Command(BaseCommand):
    ''' paloma maile management
    '''
    args = ''
    help = ''

    option_list = BaseCommand.option_list + (

        make_option('--command',
            action='store',
            dest='command',
            default='help',
            help=u'sub command'),

        make_option('--file',
            action='store',
            dest='file',
            default='stdin',
            help=u'flle'),

        make_option('--encoding',
            action='store',
            dest='encoding',
            default='utf-8',
            help=u'encoding'),
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

    def handle_help(self,con,*args,**options):
        '''  help
        '''
        import re
        for i in dir(self):
            m = re.search('^handle_(.*)$',i)
            if m == None:
                continue
            print m.group(1)

    def handle(self  ,*args, **options):
        '''  command main '''

        getattr(self, 'handle_%s'% options['command'],Command.handle_help)(*args,**options)

