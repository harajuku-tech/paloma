from django.conf import settings
from django.core.mail import get_connection
from django.utils.timezone import now
from django.template import Template,Context

from celery.task import task

from paloma.models import Schedule,Group,Mailbox,Message

CONFIG = getattr(settings, 'CELERY_EMAIL_TASK_CONFIG', {})

#: Actual Backend for sending email
BACKEND = getattr(settings, 'CELERY_EMAIL_BACKEND',
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

@task
def bounce(sender,recipient,text,is_jailed=False,*args,**kwawrs):
    ''' bounce worker '''
    import email  
    from models import Journal

    journal=None
    try:
        journal=Journal( 
            sender=sender,
            recipient=recipient,
            is_jailed=is_jailed,
            text=text)
        journal.save()
    except Exception,e:
        print e

    if is_jailed == False:
        try:
            print "TODO:class incomming mail handler" 
        except Exception,e:
            print e

@task
def trigger_schedule(sender=None):
    subject = trigger_schedule.name + ":" + str(trigger_schedule.request.id) + ":" + str(now())
    body = str(dir(trigger_schedule) )  + "\n" + str(dir(trigger_schedule.request))

    from mails import send_mail_simple
    text = str(now())
    send_mail_simple(subject,body,'triger@test.com','enqueue@test.com')        

    return True

# backwards compat
#SendEmailTask = send_email

@task
def enqueue_schedule(sender,id=None):
    ''' enqueue specifid mail schedule , or all schedules
    '''

    args={}
    if id !=None:
        args['id'] = id

    for s in Schedule.objects.filter(**args):
        if s.status== "scheduled":
            generate_messages_for_schedule(sender,s.id ) #: Asynchronized Call
            s.status = "active"
            s.save()

@task
def generate_messages_for_schedule(sender,schedule_id):
    ''' Generate messages for speicifed Schedule
    '''
    try:   
        schedule = Schedule.objects.get(id = schedule_id ) 
        for g in schedule.groups.all():
            for m in g.mailbox_set.exclude(user=None):
                #: TODO: Exclude  user == None or is_active ==False or forward == None
                generate_message(sender,schedule.id,g.id,m.id )
    except Exception,e:
        raise e

@task
def generate_message(sender,schedule_id,group_id, mailbox_id ): 
    ''' Generate (or update) message for specifed group and mailbox
    '''
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

    except Exception,e:
        raise e 
