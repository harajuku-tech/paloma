# -*- coding: utf-8 -*-
#
import os

VERSION = (0, 1, 1, 'alpha', 0)

def get_version():
    version = '%d.%d.%d' % (VERSION[0], VERSION[1], VERSION[2])
    return version

def get_logger(name='paloma'): 
    # - Python logging api 
    import logging
    return  logging.getLogger(name)

def report(msg='',exception=None,level='error',name='paloma'):
    ''' error reporting
    '''
    import traceback
    if exception:
        msg = str(exception) + "\n" + str(traceback.format_exc() )
    getattr( get_logger(name) ,level,get_logger().error)( msg )

