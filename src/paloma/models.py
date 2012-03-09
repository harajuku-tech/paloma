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

    forward_to= models.CharField(u'Forward address',max_length=100 ,default=None,null=True,blank=True)
    ''' Forward address for incomming email '''

class Group(models.Model):
    ''' Group
    '''
    owner= models.ForeignKey(Owner,verbose_name=u'Group Owner' )
    ''' Group Owner '''

    name = models.CharField(u'Group Name',max_length=100 ,db_index=True,unique=True)
    ''' Group Name '''

class Draft(models.Model):
    ''' Message Draft '''
    owner= models.ForeignKey(Owner,verbose_name=u'Draft' )
    ''' Draft '''

    subject= models.CharField(u'Subject',max_length=100 ,)
    ''' Subject '''

    text =  models.TextField(u'Text',max_length=100 ,)
    ''' Text '''

class Mailbox(models.Model):
    ''' Mailbox

        - a system user can have multiple personality
    '''
    user= models.ForeignKey(User,verbose_name=u'System User' )
    ''' System User '''

    address = models.CharField(u'Forward address',max_length=100 )
    ''' Email Address '''

    is_active = models.BooleanField(u'Actaive status',default=False )
    ''' Active Status '''

    bounces = models.IntegerField(u'Bounce counts',default=0)
    ''' Bounce count'''

class Optin(models.Model):
    ''' '''
    mailbox= models.ForeignKey(Mailbox,verbose_name=u'Mailbox' )
    ''' Mailbox '''
    groups = models.ManyToManyField(Group,verbose_name=u'Opt-in Group' )
    ''' Opt-In Group'''
    #: TODO : status (active, disabled.... )  

class Schedule(models.Model):
    ''' Message Delivery Schedule'''
    draft = models.ForeignKey(Draft ,verbose_name=u'Draft' )
    ''' Draft '''

    groups = models.ManyToManyField(Group ,verbose_name=u'Traget Groups ' )
    ''' Group '''

    dt_start =  models.DateTimeField(u'Start to send '  ,help_text=u'created datetime',default=datetime.now )
    ''' Stat datetime to send'''

    forward_to= models.CharField(u'Forward address',max_length=100 ,default=None,null=True,blank=True)
    ''' Forward address for incomming email '''

    #: TODO : other management
    #: TODO:  Filtering 
    
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
    ''' Actual Delivery 

        - Message and status management
    '''
    schedule = models.ForeignKey(Schedule,verbose_name=u'Mail Schedule' )
    ''' Mail Schedule'''
    optin= models.ForeignKey(Optin,verbose_name=u'Optin Mailboxlity' )
    ''' Optin Mailboxlit '''

    text = models.TextField(u'Message Text',default=None,blank=True,null=True)
    ''' Message text '''
    #: TODO: delivery statusm management

    objects = MessageManager()

