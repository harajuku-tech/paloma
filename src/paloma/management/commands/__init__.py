# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from optparse import make_option
from datetime import datetime
import commands
import os

class GenericCommand(BaseCommand):
    ''' paloma postfix management
    '''
    args = ''
    help = ''

    option_list = BaseCommand.option_list + (

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

        if len(args) < 3 :
            return "a sub command must be specfied"
        self.command = args[0]
        getattr(self, 'handle_%s'% self.command ,GenericCommand.handle_help)(*args,**options)
