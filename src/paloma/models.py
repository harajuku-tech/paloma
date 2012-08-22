# -*- coding: utf-8 -*-

from django.db.models import AutoField,Sum,Max ,Q
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from django.template import Template,Context

from datetime import datetime,timedelta
import sys,traceback

from paloma.utils import create_auto_secret,create_auto_short_secret

class Domain(models.Model):
    ''' Domain

        -  virtual_transport_maps.cf 
    '''
    domain = models.CharField(u'Domain',unique=True, max_length=100,db_index=True, )
    ''' Domain 

        -  key for virtual_transport_maps.cf 
        -  key and return value for  virtual_domains_maps.cf
    '''
    description = models.CharField(u'Description',max_length=200,default='')
    maxquota = models.BigIntegerField(null=True,blank=True,default=None)
    quota = models.BigIntegerField(null=True,blank=True,default=None)
    transport = models.CharField(max_length=765)
    '''  
        - virtual_transport_maps.cf   looks this for specified **domain**.
    '''

    backupmx = models.IntegerField(null=True,blank=True,default=None)
    active = models.BooleanField(default=True)
    class Meta:
        verbose_name=u'Domain'
        verbose_name_plural=u'Domains'

class Alias(models.Model):
    ''' Alias  
        - local user - maildir 
        - remote user - alias

        - for  virtual_alias_maps.cf 
    '''
    address = models.CharField(unique=True, max_length=100)
    ''' 
        - key for virtual_alias_maps.cf 
    '''
    alias = models.CharField(max_length=100,null=True,default=None,blank=True)
    '''
        - value for virtual_alias_maps.cf  
    '''
    mailbox = models.CharField(u'Mailbox',max_length=100,null=True,default=None,blank=True,
                            help_text=u'specify Maildir path if address is local user ')
    '''
        - for local usr
        - value for virtual_alias_maps.cf  
    '''
    created = models.DateTimeField(default=now)
    modified = models.DateTimeField()
    class Meta:
        pass

# - 
class AbstractProfile(models.Model):
    ''' Profile meta class'''
    class Meta:
        abstract=True

class Owner(models.Model):
    ''' Groups Owner
    '''
    user= models.ForeignKey(User,verbose_name=u'System User' )
    ''' System User '''

    name = models.CharField(u'Owner Name',max_length=100 ,db_index=True,unique=True)
    ''' Owner Name '''

    domain= models.CharField(u'@Domain',max_length=100 ,db_index=True,unique=True)
    ''' @Domain'''

    forward_to= models.CharField(u'Forward address',max_length=100 ,default=None,null=True,blank=True)
    ''' Forward address for incomming email '''

    def __unicode__(self):
        return "%s@%s" % (self.user.__unicode__(),self.domain )

class Operator(models.Model):
    ''' Operator
    '''
    owner= models.ForeignKey(Owner,verbose_name=u'Operator Owner' )
    ''' Operator Owner '''

    user= models.ForeignKey(User,verbose_name=u'System User' )
    ''' System User '''

    def __unicode__(self):
        return "%s@%s" % ( self.user.__unicode__(),self.owner.domain)

class Group(models.Model):
    ''' Group
    '''
    owner= models.ForeignKey(Owner,verbose_name=u'Group Owner' )
    ''' Group Owner '''

    name = models.CharField(u'Group Name',max_length=100 ,db_index=True )
    ''' Group Name '''

    symbol= models.CharField(u'Symbol',max_length=100 ,db_index=True ,
                    help_text=u'Used for Email address of group with owner.domain',
                    )
    ''' Symbol '''

    def __unicode__(self):
        return "%s by %s" % ( self.name,  self.owner.__unicode__() )

    @property
    def main_address(self):
        return  "%s@%s" % ( self.symbol, self.owner.domain)

    class Meta:
        unique_together = ( ('owner','name') ,
                            ('owner','symbol'),
                        )


class Mailbox(models.Model):
    ''' Mailbox

        - a system user can have multiple personality
    '''
    user= models.ForeignKey(User, verbose_name=u'System User' )
    ''' System User '''

    address = models.CharField(u'Forward address',max_length=100 ,unique=True)
    ''' Email Address 
    '''

    is_active = models.BooleanField(u'Actaive status',default=False )
    ''' Active Status '''

    bounces = models.IntegerField(u'Bounce counts',default=0)
    ''' Bounce count'''

    groups= models.ManyToManyField(Group,verbose_name=u'Opt-in Group' )
    ''' Opt-In Group'''

    def __unicode__(self):
       return "%s(%s)"% (
            self.user.__unicode__() if self.user else "unbound user",
            self.address if self.address else "not registered",
        )


class EnrollManager(models.Manager):
    ''' Enroll Manager '''

    def provide_activate(self,mailbox,group,
            viewname="paloma_enroll",absolute=lambda x : x):
        ''' Activation     
            :param mailbox: Mailbox model instance
        '''
        try:
            ret = mailbox.enroll
        except:
            ret = Enroll(mailbox=mailbox,group=group)

        ret.enroll_type = "activate" 
        ret.secret = create_auto_secret()
        ret.url = absolute(
                    reverse(viewname,
                        kwargs={"command":"activate","secret": ret.secret,})
                  )
        ret.dt_expire=now() + timedelta(minutes=3)      #:TODO
        ret.save()
        return ret

    def provide_signin(self,mailbox,group,
            viewname="paloma_enroll",absolute=lambda x: x):
        ''' Password reset or.. 
            :param mailbox: Mailbox model instance
        '''
        try:
            ret = mailbox.enroll
        except:
            ret = Enroll(mailbox=mailbox,group=group)

        ret.enroll_type = "signin" 
        ret.secret = create_auto_secret()
        ret.url = absolute(
                    reverse(viewname,
                        kwargs={"command":"signin","secret": ret.secret,})
                  )
        ret.dt_expire=now() + timedelta(minutes=3)      #:TODO
        ret.save()
        return ret

    def provide_signup(self,group):
        ''' Sing Up  
        '''
        ret = Enroll(group=group)           #:Newly created 
        ret.enroll_type = "signup" 
        ret.dt_expire=now() + timedelta(minutes=3)      #:TODO
        ret.save()
        return ret

    def provide_invite(self,group,inviter,
                        viewname="paloma_enroll",absolute=lambda x:x):
        ''' Invite
        '''
        ret = Enroll(group=group,inviter=inviter)  
        ret.enroll_type = "invite" 
        ret.dt_expire=now() + timedelta(minutes=3)      #:TODO
        ret.url = absolute(
                    reverse(viewname,
                        kwargs={"command":"invite","secret": ret.secret,})
                  )
        ret.save()
        return ret

ENROLL_TYPE = (
                ('activate','activate'),
                ('signup','signup',),
                ('signin','signin',),
                ('invite','invite',),
            )

class Enroll(models.Model):  
    ''' Enroll management 

        - Activate
        - Sign In
        - Invitation
        - Sign Up
    '''

    mailbox= models.OneToOneField(Mailbox,verbose_name=u'Mailbox' 
                    ,null=True,default=None,blank=True)
    ''' Mailbox '''

    enroll_type = models.CharField(_(u"Enroll Type"), 
                            max_length=24,db_index=True,
                            default="activate", choices=ENROLL_TYPE) 
    ''' Enroll Type '''

    group= models.ForeignKey(Group,verbose_name=u'Group' 
                    ,null=True,default=None,blank=True,
                    on_delete=models.SET_NULL)
    ''' Groupr'''

    inviter= models.ForeignKey(User,verbose_name=u'Invite' 
                    ,null=True,default=None,blank=True,
                    on_delete=models.SET_NULL)
    ''' Inviter'''

    prospect = models.CharField(u'Prospect',max_length=100,default=None,null=True,blank=True)
    ''' Prospect Email Address'''

    secret= models.CharField(u'Secret',max_length=100,default=create_auto_secret,unique=True)
    ''' Secret
    '''
    short_secret= models.CharField(u'Short Secret',max_length=10,default=create_auto_short_secret,
                unique=True)
    ''' Short Secret
    '''

    url = models.CharField(u'URL for notice',max_length=200,default=None,null=True,blank=True)
    ''' URL for notice '''


    dt_expire =   models.DateTimeField(u'Secrete Expired'  ,
                                null=True, blank=True, default=None,
                                help_text=u'Secrete Expired', )
    ''' Secrete Expired'''

    dt_try=  models.DateTimeField(u'Try Datetime'  ,
                                null=True, blank=True, default=None,
                                help_text=u'Try Datetime', )
    ''' Try Datetime'''

    dt_commit=  models.DateTimeField(u'Commit Datetime'  ,
                                null=True, blank=True, default=None,
                                help_text=u'Commit Datetime', )
    ''' Commit Datetime'''
    
    objects = EnrollManager()

    def notice(self):
        print self.group.owner.notice_set()
        
    def signup_email(self):
        return "%s-signup-%s@%s" % (
                    self.group.symbol ,
                    self.short_secret,
                    self.group.owner.domain,
                )  

    def activate(self,secret):
        pass

    def singup(self,address):
        pass

    def apply(self,secret):
        pass


class Notice(models.Model):
    ''' Notice text '''

    owner= models.ForeignKey(Owner,verbose_name=u'Owner' )
    ''' Owner'''

    name = models.CharField(u'Notice Name',max_length=20,)
    ''' Notice Name'''

    subject= models.CharField(u'Subject',max_length=100 ,)
    ''' Subject '''

    text =  models.TextField(u'Text',max_length=100 ,)
    ''' Text '''

    def render(self,*args,**kwargs):
        ''' 
            :param kwargs: Context dictionary (Group,Enroll,...)
        '''        
        return tuple([Template(t).render(Context(kwargs)) 
                for t in [self.subject,self.text] ])

class ScheduleManager(models.Manager):
    ''' Schedule Manager '''
    pass                

SCHEDULE_STATUS=(
                    ('pending','pending'),
                    ('scheduled','scheduled'),
                    ('active','active'),
                    ('finished','finished'),
                    ('canceled','canceled'),
                )

class Schedule(models.Model):
    ''' Message Delivery Schedule'''

    owner= models.ForeignKey(Owner,verbose_name=u'Owner' )
    ''' Owner'''

    subject= models.CharField(u'Subject',max_length=101 ,)
    ''' Subject '''

    text =  models.TextField(u'Text',max_length=100 ,)
    ''' Text '''

    groups = models.ManyToManyField(Group ,verbose_name=u'Traget Groups ' )
    ''' Group '''

    task= models.CharField(u'Task ID',max_length=100 ,default=None,null=True,blank=True,)
    ''' Task ID  '''

    status= models.CharField(_(u"status"), max_length=24,db_index=True,
                                default="pending", choices=SCHEDULE_STATUS) 

    dt_start =  models.DateTimeField(u'Start to send '  ,help_text=u'created datetime',default=now )
    ''' Stat datetime to send'''

    forward_to= models.CharField(u'Forward address',max_length=100 ,default=None,null=True,blank=True)
    ''' Forward address for incomming email '''

    objects = ScheduleManager()
    #: TODO : other management
    #: TODO:  Filtering 

    def __unicode__(self):
        return self.subject + self.dt_start.strftime("(%Y-%m-%d %H:%M:%S) by " + self.owner.__unicode__())

    def get_context(self,group,user):
        context = {}
        for ref in self._meta.get_all_related_objects():
            if ref.model in AbstractProfile.__subclasses__():
                try:
                    context.update( getattr(self,ref.var_name ).target_context(group,user) )
                except Exception,e:
                    pass 
        return context
    
class MessageManager(models.Manager):
    ''' Message Manager'''

    def handle_incomming_mail(self,sender,recipient,mssage ):
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

    mailbox= models.ForeignKey(Mailbox,verbose_name=u'Target Mailbox' )
    ''' Target Mailbox'''

    text = models.TextField(u'Message Text',default=None,blank=True,null=True)
    ''' Message text '''
    #: TODO: delivery statusm management

    objects = MessageManager()


class JournalManager(models.Manager):
    ''' Message Manager'''
    def handle_incomming_mail(self,sender,is_jailed,recipient,mssage ):
        ''' 
            :param mesage: :py:class:`email.Message`
        '''

class Journal(models.Model):
    ''' Raw Message

    '''
    dt_created=  models.DateTimeField(u'Journaled Datetime'  ,help_text=u'Journaled datetime', auto_now_add=True )
    ''' Journaled Datetime '''

    sender= models.CharField(u'Sender',max_length=100)
    ''' sender '''
    
    recipient= models.CharField(u'Receipient',max_length=100)
    ''' recipient '''

    text = models.TextField(u'Message Text',default=None,blank=True,null=True)
    ''' Message text '''

    is_jailed = models.BooleanField(u'Jailed Message',default=False )
    ''' Jailed(Reciepient missing emails have been journaled) if true '''

    class Meta:
        verbose_name=u'Journal'
        verbose_name_plural=u'Journals'


class EmailTaskManager(models.Manager):
    ''' EmailTaskManager'''
#    def enqueue(self,recipient,sender,journal_id):
#        """ Enqueue a email task """
#        try:
#            task = self.get(email=recipient )
#            nt = now()
#            if task.dt_expire == None or task.dt_expire > nt:
#                call_task_by_name(task_module,task_name,
#                        recipient,sender,journal_id,task.id )
#                if task.dt_expire != None:
#                    #: Expired EmalTask will be deleted by a background process.
#                    task.dt_expire = nt
#                    taks.save()
#                return True
#        except Exception,e:
#            print e 
#            pass
#
#        return False

class EmailTask(models.Model):
    """ Email Task """

    email = models.CharField(u'Email Address To Process',max_length=200,unique=True,db_index=True)
    """  Email Address to Process(Key) """

    task_module= models.CharField(u'Task Module',max_length=200,)
    """  Task Module """
    
    task_name= models.CharField(u'Task Name',max_length=200,)
    """  Task Name """

    task_key= models.CharField(u'Task Key',max_length=20,)
    """  Task Key for some entity(Depends on this task ) """

    dt_expire =   models.DateTimeField(u'Expire Datetime'  ,
                                null=True, blank=True, default=None,
                                help_text=u'Expire Datetime', )
    """ Expire Datetime """

    objects = EmailTaskManager()
