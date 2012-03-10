# -*- coding: utf-8 -*-

from django.db.models import AutoField,Sum,Max ,Q
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse

from datetime import datetime,timedelta

from paloma.models import AbstractProfile,Group,Schedule,Owner

class Company(AbstractProfile):
    ''' Company '''
    owner =  models.OneToOneField(Owner,verbose_name=u'Owner')
    
    def __unicode__(self):
        return self.owner.__unicode__()

class Shop(AbstractProfile):
    group = models.OneToOneField(Group,verbose_name=u'Shop Group')
    ''' Group bound to this shop '''

    def __unicode__(self):
        return self.group.__unicode__()

class Customer(AbstractProfile):
    ''' Customer '''
    user= models.OneToOneField(User,verbose_name=u'Customer Identity')
    ''' Customer Identity'''
    
    gender = models.IntegerField(u'Gender',choices = ((0,u'Woman'),(1,u'Man')),)
    ''' Gender '''

    def __unicode__(self):
        return self.user.__unicode__()

#####

class Product(models.Model):
    ''' Product '''
    company = models.ForeignKey(Company,verbose_name=u'Company')
    ''' Company '''
    name = models.CharField(u'Product Name',max_length=100)
    ''' Product Name '''

    def __unicode__(self):
        return self.company.__unicode__() +" " + self.name 

class Price(models.Model):
    shop= models.ForeignKey(Shop,verbose_name=u'Shop')
    ''' Shop '''    

    product = models.ForeignKey(Product,verbose_name=u'Product')
    ''' Product'''    

    price= models.DecimalField(u'Price',max_digits=5,decimal_places =0,null=True,blank=True,default=None)
    ''' Price'''    

#####
class Promotion(AbstractProfile):
    ''' Promotion '''
   
    schedule= models.OneToOneField(Schedule,verbose_name=u'Promotion Scheudle')
    ''' Promotion Schedule'''

    product = models.ForeignKey(Product,verbose_name=u'Product to promote')
    ''' Product to promote'''

    name = models.CharField(u'Promotion Name',max_length=100)
    ''' Promotio Name '''
