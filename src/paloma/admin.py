# -*- coding: utf-8 -*- 
from django.contrib import admin
from models import *

### Owner 
class OwnerAdmin(admin.ModelAdmin):
    list_display=('name','user','domain','forward_to',)
admin.site.register(Owner,OwnerAdmin)

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
    list_display=['id', 'owner', 'subject', 'text', 'dt_start', 'forward_to']
admin.site.register(Schedule,ScheduleAdmin)
### Message 
class MessageAdmin(admin.ModelAdmin):
    list_display=('schedule','mailbox',)
admin.site.register(Message,MessageAdmin)
