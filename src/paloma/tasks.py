from django.conf import settings
from django.core.mail import get_connection
from django.utils.timezone import now
from django.template import Template,Context

from celery import current_task
from celery.task import task

import logging

from paloma.models import (
        Schedule,Group,Mailbox,Message,EmailTask,
        default_return_path ,return_path_from_address
)
from paloma.mails import send_mail
from paloma.actions import EnrollAction


CONFIG = getattr(settings, 'PALOMA_EMAIL_TASK_CONFIG', {})

#: Actual Backend for sending email
BACKEND = getattr(settings, 'SMTP_EMAIL_BACKEND',
                  'django.core.mail.backends.smtp.EmailBackend')

#TASK_CONFIG = {
#    'name': 'djcelery_email_send',
#    'ignore_result': True,
#}
#TASK_CONFIG.update(CONFIG)
#

#@task(**TASK_CONFIG)
# `send_emials( list_of_messages ,**kwargs )` can be defned too,
# but that makes serialized message bigger.
@task(serializer='pickle')
def send_email(message, **kwargs):
    ''' 
    .. todo::
        - change "sennder address" for VERP 
        - kwargs should have "return_path" .
    '''
    try:
        logger = send_email.get_logger()
        conn = get_connection(backend=BACKEND)
        result = conn.send_messages([message])
        logger.debug("Successfully sent email message to %r.", message.to)
        return result
    except Exception, e:
        # catching all exceptions b/c it could be any number of things
        # depending on the backend
        logger.warning("Failed to send email message to %r, retrying.",
                    message.to)
        send_email.retry(exc=e)


def enqueue_email_task(recipient,sender,journal_id):
    """ Enqueue a email task """
    try:
        task = EmailTask.objects.get(email=recipient )
        nt = now()
        if task.dt_expire == None or task.dt_expire > nt: 
            call_task_by_name(task.task_module,task.task_name,
                    recipient,sender,journal_id,task.task_key)
            if task.dt_expire != None:
                #: Expired EmalTask will be deleted by a background process.
                task.dt_expire = nt
                tas.save()
            return True
    except Exception,e:
        print e 
        pass

    return False

def process_error_mail(recipient,sender,journal_id):
    """ Error Mail Checker and Handler

        - return True if mail was processed, owtherwise False

        :param recipient: destination mailbox address
        :type recipient: str
        :param sender: sender mailbox address
        :type recipient: str
        :param journal_id: Journal model id
        :type journal_id: int
        :rtype: bool (True : processed, False not processed)

    .. todo::
        - update journal error code or error reseon ?
    """

    if recipient in ['',None]:
        #: Simpley Error Mail!
        #: TODO: error marking... 
        return True
    
    try:
        param =  return_path_from_address(recipient)
        assert param['message_id'] != ""
        assert param['domain'] != ""
        
        try:
            #: Jourmal mail object
            journal_msg=Journal.objects.get(id=journal_id).mailobject()
            error_address= journal_msg.get('X-Failed-Recipients')
        except:
            pass

        try:
            #: Find message
            msg = Message.objects.get(id=int(param['message_id']),
                    schedule__owner__domain = param['domain'])

            #:X-Failed-Recipients SHOULD be checked ?
            assert ( error_address == None or error_address == msg.mailbox.address )

            #: increment bounce number
            #: this mailbox will be disabled sometimes later.
            msg.mailbox.bounces = msg.mailbox.bounces+ 1
            msg.mailbox.save()

            #:
            return True

        except:
            pass
            
    except exceptions.AttributeError,e:
        #:May be normal address..
        #:Other handler will be called.
        return False
         
    return False

def call_task_by_name(mod_name,task_name,*args,**kwargs):
    """ call task by name """
    
    m = __import__(mod_name,globals(),locals(),["*"])
    getattr(m,task_name).delay( *args,**kwargs)

@task 
def enroll_by_mail(recipient,sender,journal_id,key):
    """  enroll by email
    """
    print "Enroll by mail",recipient,sender,journal_id,key
    EnrollAction.enroll_by_mail(recipient,sender,journal_id,key)
    
@task
def reset_by_mail(recipient,sender,journal_id,key):
    """ reset user account by email
    """
    print "Rese User Account by mail",recipient,sender
    
@task
def ask_by_mail(recipient,sender,journal_id,key):
    """ ask by email """
    print "Ask by Email"

@task
def bounce(sender,recipient,text,is_jailed=False,*args,**kwawrs):
    """ main bounce worker
    """
    from models import Journal
    log= bounce.get_logger()

    log.debug('From=%s To %s (jailed=%s)'  % (sender,recipient,is_jailed) )

    #: First of all, save messa to the Journal
    journal=None
    try:
        journal=Journal( 
            sender=sender,
            recipient=recipient,
            is_jailed=is_jailed,
            text=text)
        journal.save()
    except Exception,e:
        log.debug( str(e) )
    
    if is_jailed == True:
        return

    #:Error Mail Handler 
    if process_error_mail(recipient,sender,journal.id):
        log.debug("no error")
        return  

    #:EmailTask ( mail registraton ....  )
    if enqueue_email_task(recipient,sender,journal.id):
        log.debug("no mail command")
        return

@task
def trigger_schedule(sender=None):
    subject = trigger_schedule.name + ":" + str(trigger_schedule.request.id) + ":" + str(now())
    body = str(dir(trigger_schedule) )  + "\n" + str(dir(trigger_schedule.request))

    from mails import send_mail_simple
    text = str(now())
    send_mail_simple(subject,body,'triger@test.com','enqueue@test.com')        

    return True

@task
def enqueue_schedule(sender,id=None):
    ''' enqueue specifid mail schedule , or all schedules
    '''
    log = current_task.get_logger()

    args={'id':id} if id else {}
    log.debug("specified Schedule id = %s" % str(args))

    for s in Schedule.objects.filter(**args):
        if s.status== "scheduled":
            generate_messages_for_schedule.delay(sender,s.id ) #: Asynchronized Call
            s.status = "active"
            s.save()

@task
def generate_messages_for_schedule(sender,schedule_id):
    ''' Generate messages for speicifed Schedule
    '''
    log = current_task.get_logger()
    try:   
        schedule = Schedule.objects.get(id = schedule_id ) 
        for g in schedule.groups.all():
            for m in g.mailbox_set.exclude(user=None):
                #: TODO: Exclude  user == None or is_active ==False or forward == None
                generate_message.delay(sender,schedule.id,g.id,m.id )
    except Exception,e:
        log.error( "generate_messages_for_schedule():" +  str(e) )

@task
def generate_message(sender,schedule_id,group_id, mailbox_id ): 
    ''' Generate (or update) message for specifed group and mailbox
    '''
    log = current_task.get_logger()
    current_time = now()
    try:
        schedule = Schedule.objects.get(id=schedule_id )
        group = Group.objects.get(id=group_id)
        mailbox= Mailbox.objects.get(id=mailbox_id)

        context = schedule.get_context(group,mailbox.user)        
        msg=None
        try:
            msg = Message.objects.get(schedule=schedule,mailbox=mailbox )
        except Exception,e:
            msg = Message(schedule=schedule,mailbox=mailbox )

        msg.text = Template(schedule.text).render(Context(context))
        msg.save()

        if current_time >= schedule.dt_start: #:TODO : 1 minutes 
            #: sendmail right now
            send_message(message_obj=msg) 
        else :
            #: sendmail later
            send_message.apply_async([msg.id],eta=msg.dt_start )

    except Exception,e:
        log.error("generate_message()" + str(e))

@task
def send_message(message_id=None,message_obj=None):
    ''' send actual message
        
    .. todo::
        - Message status is required
    '''
    log = current_task.get_logger()
    try:
        msg = message_obj if message_obj != None else Messsage.objects.get(id=message_id) 
        #:TODO: check message status. If already "SENDING" or "CANCELD", don't send
        #       check schedue status. If already "CANCELD", don't send
        send_mail(msg.schedule.subject,     #:TODO: Message should have rendered subject
                  msg.text,
                  "info@"+msg.schedule.owner.domain, #:TODO: Owner "symbol" to be defined and compose from address
                  [msg.mailbox.address],
                  return_path = msg.get_return_path(),
                  message_id = msg.mail_message_id,
            )
        #:TODO: change the status
                  
    except Message.DoesNotExist ,e:
        log.error("send_message():No Message record for id=%s" % message_id)
    except Exception,e:
        #: STMP error... ?
        log.error("send_message(): %s" % str(e))
        #:TODO: 
        #   - error message to Message
        #   - change status of Message
        
@task
def disable_mailbox(bounce_count=None,*args,**kwargs):
    '''  

        :param bounce_count:  number of error mail bounced back.
        :type  bounce_count:  int
    '''
    log = disable_mailbox.get_logger()

    if bounce_count:
        ret = Mailbox.objects.filter(bounces__gte=bounce_count).update(is_active=False)
        log.debug( "diabble_mailbox: %d mailboxes have been diabled." % ret )
            
