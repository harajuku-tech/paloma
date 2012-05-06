from django.db import models

class Admin(models.Model):
    username = models.CharField(max_length=765)
    password = models.CharField(max_length=765)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    active = models.IntegerField()
    class Meta:
        pass

class Alias(models.Model):
    address = models.CharField(unique=True, max_length=765)
    goto = models.TextField()
    domain = models.CharField(max_length=765)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    active = models.IntegerField()
    class Meta:
        pass

class AliasDomain(models.Model):
    alias_domain = models.CharField(unique=True, max_length=765)
    target_domain = models.CharField(max_length=765)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    active = models.IntegerField()
    class Meta:
        pass

class Config(models.Model):
    name = models.CharField(unique=True, max_length=60)
    value = models.CharField(max_length=60)
    class Meta:
        pass

class Domain(models.Model):
    domain = models.CharField(unique=True, max_length=765)
    description = models.CharField(max_length=765)
    aliases = models.IntegerField()
    mailboxes = models.IntegerField()
    maxquota = models.BigIntegerField()
    quota = models.BigIntegerField()
    transport = models.CharField(max_length=765)
    backupmx = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    active = models.IntegerField()
    class Meta:
        pass

class DomainAdmins(models.Model):
    username = models.CharField(max_length=765)
    domain = models.CharField(max_length=765)
    created = models.DateTimeField()
    active = models.IntegerField()
    class Meta:
        pass

class Fetchmail(models.Model):
    mailbox = models.CharField(max_length=765)
    src_server = models.CharField(max_length=765)
    src_auth = models.CharField(max_length=33, blank=True)
    src_user = models.CharField(max_length=765)
    src_password = models.CharField(max_length=765)
    src_folder = models.CharField(max_length=765)
    poll_time = models.IntegerField()
    fetchall = models.IntegerField()
    keep = models.IntegerField()
    protocol = models.CharField(max_length=12, blank=True)
    usessl = models.IntegerField()
    extra_options = models.TextField(blank=True)
    returned_text = models.TextField(blank=True)
    mda = models.CharField(max_length=765)
    date = models.DateTimeField()
    class Meta:
        pass

class Log(models.Model):
    timestamp = models.DateTimeField()
    username = models.CharField(max_length=765)
    domain = models.CharField(max_length=765)
    action = models.CharField(max_length=765)
    data = models.TextField()
    class Meta:
        pass

class Mailbox(models.Model):
    username = models.CharField(unique=True, max_length=765)
    password = models.CharField(max_length=765)
    name = models.CharField(max_length=765)
    maildir = models.CharField(max_length=765)
    quota = models.BigIntegerField()
    local_part = models.CharField(max_length=765)
    domain = models.CharField(max_length=765)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    active = models.IntegerField()
    class Meta:
        pass

class Quota(models.Model):
    username = models.CharField(unique=True, max_length=765)
    path = models.CharField(unique=True, max_length=300)
    current = models.BigIntegerField(null=True, blank=True)
    class Meta:
        pass

class Quota2(models.Model):
    username = models.CharField(unique=True, max_length=300)
    bytes = models.BigIntegerField()
    messages = models.IntegerField()
    class Meta:
        pass

class Vacation(models.Model):
    email = models.CharField(unique=True, max_length=765)
    subject = models.CharField(max_length=765)
    body = models.TextField()
    cache = models.TextField()
    domain = models.CharField(max_length=765)
    created = models.DateTimeField()
    active = models.IntegerField()
    class Meta:
        pass

class VacationNotification(models.Model):
    on_vacation = models.ForeignKey(Vacation, db_column='on_vacation')
    notified = models.CharField(unique=True, max_length=765)
    notified_at = models.DateTimeField()
    class Meta:
        pass
