# -*- coding: utf-8 -*- 
from django.contrib import admin
from models import *

### Owner 
class OwnerAdmin(admin.ModelAdmin):
    pass
admin.site.register(Owner,OwnerAdmin)
### Group 
class GroupAdmin(admin.ModelAdmin):
    pass
admin.site.register(Group,GroupAdmin)
### Draft 
class DraftAdmin(admin.ModelAdmin):
    pass
admin.site.register(Draft,DraftAdmin)
### Schedule 
class ScheduleAdmin(admin.ModelAdmin):
    pass
admin.site.register(Schedule,ScheduleAdmin)
### Mailbox 
class MailboxAdmin(admin.ModelAdmin):
    pass
admin.site.register(Mailbox,MailboxAdmin)
### Optin 
class OptinAdmin(admin.ModelAdmin):
    pass
admin.site.register(Optin,OptinAdmin)
### Message 
class MessageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Message,MessageAdmin)
