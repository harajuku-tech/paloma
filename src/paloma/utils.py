# -*- coding: utf-8 -*-

import random ,os
import string
from datetime import datetime 

def gen_random_string(length, chrs=None):
    ''' generate random string

        :param length: length of generated string 
        :param chrs:  character restriction
    '''

    if chrs is None:
        return os.urandom(length) 
    else:
        return ''.join([chrs[ random.SystemRandom().randrange(len(chrs))] 
                    for _ in xrange(length)])

def gen_nonce(when=None):
    ''' generate nonce 

        :param when: datetime
    '''
    NONCE_CHARS = string.ascii_letters + string.digits
    salt = gen_random_string(6, NONCE_CHARS)
        
    when = when if when else datetime.now() 
    return  when.strftime('%Y%m%d%H%M%S%f'+salt)

def create_auto_secret():
    ''' create auto secret '''
    SECRET_CHARS = string.ascii_letters + string.digits
    return gen_random_string(32,SECRET_CHARS)

def create_auto_short_secret():
    ''' create auto short secret '''
    SECRET_CHARS = string.ascii_letters + string.digits
    return gen_random_string(8,SECRET_CHARS)
