# -*- coding: utf-8 -*-

from django.core.mail import send_mail
from email import message_from_file

def send_mail_simple(subject,text,addr_from, addr_to ):
    ''' Send simple email '''
    addr_to = addr_to if type(addr_to) == list else [addr_to]
    send_mail(subject,text, addr_from,addr_to ) 

def send_mail_from_file(stream):
    ''' Send an email from file
    '''
    if type(stream) == str:
        stream = open(stream)
    msg = message_from_file(stream)
    send_mail(msg['Subject'],str(msg),msg['From'],msg['To'].split(',') )
