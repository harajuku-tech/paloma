# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from optparse import make_option
from datetime import datetime
import commands
import sys
import os

class GenericCommand(BaseCommand):
    ''' paloma postfix management
    '''
    args = ''
    help = ''
    model=None

    option_list = BaseCommand.option_list + (

        make_option('--id',
            action='store',
            dest='id',
            default=None,
            help=u'entity id(message,user,...'),

        make_option('-s','--sync',
            action='store_true',
            dest='sync',
            default=False,
            help=u'Synchronous Call'),

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

    def open_file(self,options):
        fp = sys.stdin if options['file'] == 'stdin' else open(options['file'])
        return fp

    def handle_count(self,*args,**option):
        if self.model:
            print self.model,self.model.objects.count()
        
    def handle_help(self,*args,**options):
        '''  help
        '''
        import re
        for i in dir(self):
            m = re.search('^handle_(.*)$',i)
            if m == None:
                continue
            print m.group(1)
        print args
        print options

    def handle(self  ,*args, **options):
        '''  command main '''

        if len(args) < 1 :
            return "a sub command must be specfied"
        self.command = args[0]
        getattr(self, 'handle_%s'% self.command ,GenericCommand.handle_help)(*args,**options)
