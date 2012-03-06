# -*- coding: utf-8 -*-

from paloma.management.commands import GenericCommand

class Command(GenericCommand):
    ''' bouncer
    '''
    
    def handle_main(self,*args,**options):
        ''' main '''
        print "bouncer main"

    def handle(self  ,*args, **options):
        '''  command main '''
        getattr(self, 'handle_%s'% options['command'],Command.handle_help)(*args,**options)

