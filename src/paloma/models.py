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
    #: TODO : other management
    #: TODO:  Filtering 
    
class Member(models.Model):
    user= models.ForeignKey(User,verbose_name=u'System User' )
    ''' System User '''
    groups = models.ManyToManyField(Group,verbose_name=u'Opt-in Group' )
    #: TODO : status (active, disabled.... )  
    
class Message(models.Model):
    ''' Actual Delivery '''
    schedule = models.ForeignKey(Schedule,verbose_name=u'Mail Schedule' )
    member= models.ForeignKey(User,verbose_name=u'Member' )
    text = models.TextField(u'Message Text',default=None,blank=True,null=True)
    #: TODO: delivery statusm management

