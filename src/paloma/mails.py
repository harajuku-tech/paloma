# -*- coding: utf-8 -*-

from django.core.mail import send_mail

def send_mail_simple(subject,addr_from, addr_to ):
    ''' Send simple email '''
    addr_to = addr_to if type(addr_to) == list else [addr_to]
    send_mail(subject, addr_from,addr_to ) 
