# -*- coding: utf-8 -*-

from paloma.management.commands import GenericCommand
from paloma.mails import send_mail,send_mail_from_file

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
        send_mail_from_file( self.open_file(options) )

    def handle_help(self,*args,**options):
        '''  help
        '''
        import re
        for i in dir(self):
            m = re.search('^handle_(.*)$',i)
            if m == None:
                continue
            print m.group(1)
