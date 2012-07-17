# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from optparse import make_option
from datetime import datetime
import commands
import os

from paloma.management.commands import GenericCommand

class Command(GenericCommand):
    ''' paloma maile management
    '''
    args = ''
    help = ''

    option_list = GenericCommand.option_list + (

        make_option('--command',
            action='store',
            dest='command',
            default='help',
            help=u'sub command'),
        )
    ''' Command Option '''

    def handle_enqueue(self,*args,**options):
        '''　enqueue

        '''
        if options['id'].isdigit():
            print "Specified Schedule" , options['id']
        else:
            print "All Schedule"

