# -*- coding: utf-8 -*-

from django.db.models import AutoField,Sum,Max ,Q
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from django.core.mail import send_mail

from django.template import Template,Context

from datetime import datetime,timedelta
import sys,traceback

from paloma.utils import create_auto_secret,create_auto_short_secret
from paloma.models import Enroll,EmailTask,Mailbox

class Action(object):
    def __init__(self,request=None):
        ''' 
            :param request: WSGI request
        '''  
        self.request = request

    def absolute(self,url):
        ''' absoute url '''
        return self.request.build_absolute_uri(url)  \
                if self.request else url

class EnrollAction(Action):
    ''' Enroll Action'''

    def provide_activate(self,mailbox,group, viewname="paloma_enroll" ):
        ''' Activation     
            :param mailbox: Mailbox model instance
        '''
        try:
            ret = mailbox.enroll
        except:
            ret = Enroll(mailbox=mailbox,group=group)

        ret.enroll_type = "activate" 
        ret.secret = create_auto_secret()
        ret.url = self.absolute(
                    reverse(viewname,
                        kwargs={"command":"activate","secret": ret.secret,})
                  )
        print ret.url
        ret.dt_expire=now() + timedelta(minutes=3)      #:TODO
        ret.save()
        return ret

    def provide_signin(self,mailbox,group, viewname="paloma_enroll"):
        ''' Password reset or.. 
            :param mailbox: Mailbox model instance
        '''
        try:
            ret = mailbox.enroll
        except:
            ret = Enroll(mailbox=mailbox,group=group)

        ret.enroll_type = "signin" 
        ret.secret = create_auto_secret()
        ret.url = self.absolute(
                    reverse(viewname,
                        kwargs={"command":"signin","secret": ret.secret,})
                  )
        ret.dt_expire=now() + timedelta(minutes=3)      #:TODO
        ret.save()
        return ret

    def provide_signup(self,group):
        ''' Sign Up  
        '''
        ret = Enroll(group=group)           #:Newly created 
        ret.enroll_type = "signup" 
        ret.dt_expire=now() + timedelta(minutes=3)      #:TODO
        ret.save()

        #:Emai Task
        et = EmailTask(email =ret.signup_email(),       
                        task_module="paloma.tasks",
                        task_name="enroll_by_mail",
                        task_key = str(ret.id),
                        dt_expire = now() + timedelta(minutes=3)
                )
        et.save()

        return ret

    def provide_invite(self,group,inviter,
                        viewname="paloma_enroll",absolute=lambda x:x):
        ''' Invite
        '''
        ret = Enroll(group=group,inviter=inviter)  
        ret.enroll_type = "invite" 
        ret.dt_expire=now() + timedelta(minutes=3)      #:TODO
        ret.url = self.absolute(
                    reverse(viewname,
                        kwargs={"command":"invite","secret": ret.secret,})
                  )
        ret.save()
        return ret

    def enroll_by_web(self,username,password,email,group ):
        ''' enroll by web
        '''
        #: System user
        user = User.objects.create_user(username,email,password)

        #: create MailBox bound to the Django User  
        mailbox = Mailbox(user =user,
                        address =email,
                        is_active =False,
                       ) 
        mailbox.save()

        #: add group  to the Mailbox
        mailbox.groups.add(group)

        #: for activateion
        el = self.provide_activate(mailbox,group)

        #:Sending Greeting Email
        qs = group.owner.notice_set.filter(name="activate")
        if qs.count() > 0 :
            (subject,text ) = qs[0].render(enroll=el, group=group )
            send_mail(subject,text, group.main_address , [ mailbox.address ])
        
    def enroll_by_mail(self,recipient,sender,journal_id,key):
        '''  enroll by email
        '''
        e =  Enroll.objects.get(id=key)
       
        #: Create Django User with random password
        user = User.objects.create_user(sender,
                    sender,
                    User.objects.make_random_password())
        
        #: create MailBox bound to the Django User  
        mailbox = Mailbox(user =user,
                        address =sender,
                        is_active =True,
                       ) 
        mailbox.save()

        #: add group  to the Mailbox
        mailbox.groups.add(e.group)

        #: TODO: send greeting Notice

        #: update time
        e.dt_try = now()
        e.save() 

    def activate(self,secret):
        ''' Activate account '''
        ret = Enroll.objects.get(enroll_type = "activate",
                                secret = secret )
        if ret.is_open() ==False:
            return None
        #:User
        ret.mailbox.user.is_active = True
        ret.mailbox.user.save()

        #:Mailbox
        ret.mailbox.is_active=True 
        ret.mailbox.save()

        ret.close()

        return ret
