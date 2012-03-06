# -*- coding: utf-8 -*-

from paloma.management.commands import GenericCommand
from optparse import make_option

class Command(GenericCommand):
    ''' bouncer
    '''

    option_list = GenericCommand.option_list + ( 

        make_option('--async',
            action='store',
            dest='async',
            default=True,
            help=u'Process asynchronously with message queue'),

        )   

    def handle_main(self,*args,**options):
        ''' main '''
        import sys
        if sys.stdin.isatty():
            #: no stdin
            print "no stdin...."
            return

        from paloma.tasks import bounce 
        if options['async']==True:
            print "celeryed"
            bounce.delay(''.join(sys.stdin.read()) ) #:message queuing
        else:
            bounce(''.join(sys.stdin.read()) ) #: synchronous call for testing

    def handle(self  ,*args, **options):
        '''  command main '''
        getattr(self, 'handle_%s'% options['command'],Command.handle_help)(*args,**options)

