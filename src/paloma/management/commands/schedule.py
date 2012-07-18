# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from optparse import make_option
from datetime import datetime
import commands
import os

from paloma.management.commands import GenericCommand
from paloma.models import Schedule 
from paloma.tasks import enqueue_schedule

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

        if options['sync']:
            Schedule.objects.enqueue_messages( options['id'] )
        else:
            enqueue_schedule.delay(options['id'])
