# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from optparse import make_option
from datetime import datetime
import commands
import os

from paloma.management.commands import GenericCommand
from paloma.models import Message

class Command(GenericCommand):
    ''' paloma maile management
    '''
    args = ''
    help = ''
    model=Message

    option_list = GenericCommand.option_list + (
        )
    ''' Command Option '''

    def handle_remove(self,*args,**options):
        '''　remove messages

        '''
        if options['id'] and options['id'].isdigit():
            try:
                Message.objects.get(id=options['id']).delete()
            except Exception,e:
                print "*** Cant remove message for ",options['id'] 
                print e
        else:
            Message.objects.all().delete()

