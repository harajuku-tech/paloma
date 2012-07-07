#-*- coding: utf-8 -*-
import os
# - configure logging

def config(LOGGING):
    '''  configure logging facility

    >>> import applogs
    >>> applogs.config(LOGGING)

        - level 

            DEBUG: Low level system information for debugging purposes
            INFO: General system information
            WARNING: Information describing a minor problem that has occurred.
            ERROR: Information describing a major problem that has occurred.
            CRITICAL: Information describing a critical problem that has occurred.
    '''
    #: custom formatter
    if not LOGGING.has_key('formatters') : 
        LOGGING['formatters']={} 
        
    LOGGING['formatters']['parsefriendly'] = { 
        'format': '[%(levelname)s] %(asctime)s - M:%(module)s, P:%(process)d, T:%(thread)d, MSG:%(message)s',
        'datefmt': '%d/%b/%Y:%H:%M:%S %z',
    }

    #  customer handler (console)
    LOGGING['handlers']['console'] = { 
        'level':    'DEBUG',
        'class':    'logging.StreamHandler',
        'formatter':'parsefriendly',
    }

    #  customer handler (file)
    LOGGING['handlers']['file'] = { 
        'level':    'DEBUG',
        'class':    'logging.handlers.TimedRotatingFileHandler', 
        'formatter':'parsefriendly',
        'when':     'midnight',
        'filename': os.environ.get('APP_LOGGER_FILE','/tmp/app.log'),
    }

    #  customer logger (dev)
    LOGGING['loggers']['dev'] = { 
        'handlers': ['console'],
        'level':    'DEBUG', 
#        'level':    'CRITICAL', 
        'propagete':    True,
    }

    #  customer logger (live)
    LOGGING['loggers']['live'] = { 
        'handlers': ['file'],
#        'level':    'WARNING', 
        'level':    'DEBUG', 
        'propagete':    True,
    }

    # - paloma logging handler -----

    LOGGING['handlers']['paloma'] = { 
        'level':    'DEBUG',
        'class':    'logging.handlers.TimedRotatingFileHandler', 
        'formatter':'parsefriendly',
        'when':     'midnight',
        'filename': os.environ.get('PALOMA_LOGGER_FILE','/tmp/paloma.log'),
    }

    LOGGING['loggers']['paloma'] = { 
        'handlers': ['paloma'],
#        'level':    'WARNING', 
        'level':    'DEBUG', 
        'propagete':    True,
    }

def get_logger():
    ''' application logger 
    >>> import applogs
    >>> logger = applogs.get_logger()
    >>> logger.debug('An exception is raised')
    '''
    # - Python logging api 
    import logging
    return  logging.getLogger(os.environ.get('APP_LOGGER','live'))

def report(exception,level='error'):
    ''' exception report utility
    '''
    import traceback
    getattr(get_logger(),level)( str(traceback.format_exc()) )
