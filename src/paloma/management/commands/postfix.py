# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from optparse import make_option
from datetime import datetime
import commands
import os

class Command(BaseCommand):
    ''' paloma postfix management
    '''
    args = ''
    help = ''

    option_list = BaseCommand.option_list + (

        make_option('--command',
            action='store',
            dest='command',
            default='help',
            help=u'sub command'),

        make_option('--id',
            action='store',
            dest='id',
            default='help',
            help=u'message id'),

        make_option('--encoding',
            action='store',
            dest='encoding',
            default='utf-8',
            help=u'encoding'),
        )
    ''' Command Option '''

    def handle_qlist(self,*args,**options):
        '''　qlist

        '''
        import commands
        import re
        item = [ 
                r'^(?P<id>.+)',
                r'(?P<size>\d+)',
                r'(?P<day>.+)',
                r'(?P<month>.+)',
                r'(?P<date>\d+)',
                r'(?P<time>\d{2}:\d{2}:\d{2})',
                r'(?P<from>.+)$',
            ]
        pat = re.compile('\\s' .join(item))

        for l in commands.getoutput('mailq').split('\n'):
            s = pat.search(l)  
            if s : 
                print l

    def handle_delete(self,*args,**options):
        ''' delete message from queue '''
        options['id']= options['id'].replace('*','')
        print commands.getoutput('sudo  postsuper -d %(id)s' % options )
        
    def handle_help(self,*args,**options):
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

