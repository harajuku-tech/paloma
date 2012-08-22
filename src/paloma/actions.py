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
from paloma.models import Enroll,EmailTask,Mailbox

class EnrollAction:
    ''' Enroll Action'''

    @classmethod
    def provide_activate(cls,mailbox,group,
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

    @classmethod
    def provide_signin(cls,mailbox,group,
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

    @classmethod
    def provide_signup(cls,group):
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

    @classmethod
    def provide_invite(cls,group,inviter,
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

    @classmethod
    def enroll_by_web(cls,username,password,email,group ):
        ''' enroll by web
        '''
        user = User.objects.create_user(username,email,password)
        #: create MailBox bound to the Django User  
        mailbox = Mailbox(user =user,
                        address =email,
                        is_active =False,
                       ) 
        mailbox.save()

        #: add group  to the Mailbox
        mailbox.groups.add(group)

        #:Sending Greeting Email
        
    @classmethod
    def enroll_by_mail(cls,recipient,sender,journal_id,key):
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
