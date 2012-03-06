# -*- coding: utf-8 -*-

from django.db.models import AutoField,Sum,Max ,Q
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse

from datetime import datetime,timedelta

class AbstractProfile(models.Model):
    ''' Profile meta class'''
    class Meta:
        abstract=True

class Owner(models.Model):
    ''' Group Owner
    '''
    user= models.ForeignKey(User,verbose_name=u'System User' )
    ''' System User '''

class Group(models.Model):
    ''' Group
    '''
    owner= models.ForeignKey(Owner,verbose_name=u'Group Owner' )

class Draft(models.Model):
    ''' Message Draft '''
    owner= models.ForeignKey(Owner,verbose_name=u'Draft' )
    ''' Draft '''

class Schedule(models.Model):
    ''' Message Delivery Schedule'''
    draft = models.ForeignKey(Draft ,verbose_name=u'Draft' )
    groups = models.ManyToManyField(Group ,verbose_name=u'Traget Groups ' )

    dt_start =  models.DateTimeField(u'Start to send '  ,help_text=u'created datetime',default=datetime.now )

    forward_to= models.CharField(u'Forward address',max_length=100 ,default=None,null=True,blank=True)
    ''' Forward address for incomming email '''
    #: TODO : other management
    #: TODO:  Filtering 
    
class Member(models.Model):
    user= models.ForeignKey(User,verbose_name=u'System User' )
    ''' System User '''
    groups = models.ManyToManyField(Group,verbose_name=u'Opt-in Group' )
    #: TODO : status (active, disabled.... )  

class MessageManager(models.Manager):
    ''' Message Manager'''
    def handle_incomming_mail(self,mssage ):
        ''' 
            :param mesage: :py:class:`email.Message`
        ''' 
        print "Welcom to Mesage processor" 
        #: TODO
        #: 1. check "to" address
        #:      - Find Owner with domain
        #:          - no Owner?, forward to system error email
        #:
        #: 2. any special mail, call handler
        #:      - Sign up try
        #:      - Sign Up
        #:      - Close account
        #:      - .....
        #:
        #: 3 if a Message of whose destination is qual to "to" is found, 
        #:      that Message is error bounced
        #:      
        #:      -   check if message is spma of not
        #:          - with Mailman's spam checker or others
        #:      - (check the error ... )
        #:      - flag the target Member as "bounced"
        #:          - Member should not be targeted on the next schedule.         
        #:
        #: 4. If Schedule has forward_to:
        #:      - send message to forward_to
        #:
        #: 5. otherwise, do nothing. 
        pass
    
class Message(models.Model):
    ''' Actual Delivery '''
    schedule = models.ForeignKey(Schedule,verbose_name=u'Mail Schedule' )
    member= models.ForeignKey(User,verbose_name=u'Member' )
    text = models.TextField(u'Message Text',default=None,blank=True,null=True)
    #: TODO: delivery statusm management

    objects = MessageManager()

