# -*- coding: utf-8 -*- 
from django.contrib import admin
from models import *
from django.conf import settings

if settings.DEBUG:
    try:
        from djkombu.models import Queue as KombuQueue,Message as KombuMessage
        from djcelery.models import TaskMeta,TaskSetMeta

        ### KombuQueue
        class KombuQueueAdmin(admin.ModelAdmin):
            list_display=tuple([f.name for f in KombuQueue._meta.fields ])
        admin.site.register(KombuQueue,KombuQueueAdmin)
        
        ### define __unicode__ to Queue class
        #
        #def __unicode__(self):
        #
        #   return self.name

        ### KombuMessage
        class KombuMessageAdmin(admin.ModelAdmin):
            list_display=tuple([f.name for f in KombuMessage._meta.fields])
        admin.site.register(KombuMessage,KombuMessageAdmin)

        ### TaskMeta
        class TaskMetaAdmin(admin.ModelAdmin):
            list_display=tuple([f.name for f in TaskMeta._meta.fields])
            list_filter = ('status',)
            date_hierarchy = 'date_done'
        admin.site.register(TaskMeta,TaskMetaAdmin)
        
        ### TaskSetMeta
        class TaskSetMetaAdmin(admin.ModelAdmin):
            list_display=tuple([f.name for f in TaskSetMeta._meta.fields])
        admin.site.register(TaskSetMeta,TaskSetMetaAdmin)
        
        
    except Exception,e:
        print e
        pass

### Domain 
class DomainAdmin(admin.ModelAdmin):
    list_display=tuple([f.name for f in Domain._meta.fields ])
admin.site.register(Domain,DomainAdmin)

### Alias 
class AliasAdmin(admin.ModelAdmin):
    list_display=tuple([f.name for f in Alias._meta.fields ])
admin.site.register(Alias,AliasAdmin)


### Owner 
class OwnerAdmin(admin.ModelAdmin):
    list_display=('name','user','domain','forward_to',)
admin.site.register(Owner,OwnerAdmin)

### Operator 
class OperatorAdmin(admin.ModelAdmin):
    list_display=('owner','user', )
admin.site.register(Operator,OperatorAdmin)

### Group 
class GroupAdmin(admin.ModelAdmin):
    list_display=('name','owner','symbol','main_address')
    list_filter=('owner',)
admin.site.register(Group,GroupAdmin)

### Mailbox 
class MailboxAdmin(admin.ModelAdmin):
    list_display=('id', 'user', 'address', 'is_active', 'bounces' )
admin.site.register(Mailbox,MailboxAdmin)

### Schedule 
class ScheduleAdmin(admin.ModelAdmin):
    list_display=['id', 'owner', 'subject', 'text', 'dt_start', 'forward_to','task',]
admin.site.register(Schedule,ScheduleAdmin)
### Message 
class MessageAdmin(admin.ModelAdmin):
    list_display=('schedule','mailbox',)
admin.site.register(Message,MessageAdmin)

### Journal 
class JournalAdmin(admin.ModelAdmin):
    list_display=tuple([f.name for f in Journal._meta.fields ])
admin.site.register(Journal,JournalAdmin)

