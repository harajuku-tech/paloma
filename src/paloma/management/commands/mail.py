# -*- coding: utf-8 -*-

from paloma.management.commands import GenericCommand
from paloma.mails import send_mail_simple,send_mail_from_file
from paloma.tasks import trigger_schedule

from django.utils import timezone, dateparse

from optparse import make_option
from datetime import datetime
import commands
import os
import uuid

class Command(GenericCommand):
    ''' paloma maile management
    '''
    args = ''
    help = ''

    option_list = GenericCommand.option_list + (

        make_option('-t','--time',
            action='store',
            dest='time',
            default=None,
            help=u'time to trigger'),

        make_option('-r','--return_path',
            action='store',
            dest='return_path',
            default=None,
            help=u'mailbox to be returned'),
        )
    ''' Command Option '''

    def handle_send(self,*args,**options):
        '''　send

        '''
        extra = { "return_path" : options.get('return_path',None), 
                  "message_id"  : "paloma-%s" % uuid.uuid1().hex, 
                } 
        send_mail_from_file( self.open_file(options), **extra )

    def handle_trigger(self,*args,**options):
        ''' trigger schedule
        '''
        if options['time'] != None:
            eta = timezone.make_aware( 
                    dateparse.parse_datetime(options['time']) ,
                    timezone.get_current_timezone())
        else :
            eta=None 
        t=trigger_schedule.apply_async(eta=eta)
        print "Task is scheduled.id=",t.id

    def handle_help(self,*args,**options):
        '''  help
        '''
        import re
        for i in dir(self):
            m = re.search('^handle_(.*)$',i)
            if m == None:
                continue
            print m.group(1)
