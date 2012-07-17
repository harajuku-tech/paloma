# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from optparse import make_option
from datetime import datetime
import commands
import os

from paloma.management.commands import GenericCommand
from paloma.models import Schedule 

class Command(GenericCommand):
    ''' paloma schedule management
    '''
    args = ''
    help = ''
    model= Schedule

    option_list = GenericCommand.option_list + (
        )

    def handle_enqueue(self,*args,**options):
        '''　enqueue messages from schedules

        '''

        if options['id'].isdigit():
            print "Specified Schedule" , options['id']
        else:
            for s in Schedule.objects.all(): 
                s.generate_messages()

