# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Domain'
        db.create_table('paloma_domain', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('domain', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100, db_index=True)),
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('maxquota', self.gf('django.db.models.fields.BigIntegerField')(default=None, null=True, blank=True)),
            ('quota', self.gf('django.db.models.fields.BigIntegerField')(default=None, null=True, blank=True)),
            ('transport', self.gf('django.db.models.fields.CharField')(max_length=765)),
            ('backupmx', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('paloma', ['Domain'])

        # Adding model 'Alias'
        db.create_table('paloma_alias', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('goto', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True, blank=True)),
            ('maildir', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('paloma', ['Alias'])

        # Adding model 'Owner'
        db.create_table('paloma_owner', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100, db_index=True)),
            ('domain', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100, db_index=True)),
            ('forward_to', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('paloma', ['Owner'])

        # Adding model 'Group'
        db.create_table('paloma_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['paloma.Owner'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
        ))
        db.send_create_signal('paloma', ['Group'])

        # Adding unique constraint on 'Group', fields ['owner', 'name']
        db.create_unique('paloma_group', ['owner_id', 'name'])

        # Adding unique constraint on 'Group', fields ['owner', 'symbol']
        db.create_unique('paloma_group', ['owner_id', 'symbol'])

        # Adding model 'Mailbox'
        db.create_table('paloma_mailbox', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('bounces', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('paloma', ['Mailbox'])

        # Adding M2M table for field groups on 'Mailbox'
        db.create_table('paloma_mailbox_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mailbox', models.ForeignKey(orm['paloma.mailbox'], null=False)),
            ('group', models.ForeignKey(orm['paloma.group'], null=False))
        ))
        db.create_unique('paloma_mailbox_groups', ['mailbox_id', 'group_id'])

        # Adding model 'Schedule'
        db.create_table('paloma_schedule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['paloma.Owner'])),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=101)),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=100)),
            ('dt_start', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('forward_to', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('paloma', ['Schedule'])

        # Adding M2M table for field groups on 'Schedule'
        db.create_table('paloma_schedule_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('schedule', models.ForeignKey(orm['paloma.schedule'], null=False)),
            ('group', models.ForeignKey(orm['paloma.group'], null=False))
        ))
        db.create_unique('paloma_schedule_groups', ['schedule_id', 'group_id'])

        # Adding model 'Message'
        db.create_table('paloma_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['paloma.Schedule'])),
            ('mailbox', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['paloma.Mailbox'])),
            ('text', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal('paloma', ['Message'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Group', fields ['owner', 'symbol']
        db.delete_unique('paloma_group', ['owner_id', 'symbol'])

        # Removing unique constraint on 'Group', fields ['owner', 'name']
        db.delete_unique('paloma_group', ['owner_id', 'name'])

        # Deleting model 'Domain'
        db.delete_table('paloma_domain')

        # Deleting model 'Alias'
        db.delete_table('paloma_alias')

        # Deleting model 'Owner'
        db.delete_table('paloma_owner')

        # Deleting model 'Group'
        db.delete_table('paloma_group')

        # Deleting model 'Mailbox'
        db.delete_table('paloma_mailbox')

        # Removing M2M table for field groups on 'Mailbox'
        db.delete_table('paloma_mailbox_groups')

        # Deleting model 'Schedule'
        db.delete_table('paloma_schedule')

        # Removing M2M table for field groups on 'Schedule'
        db.delete_table('paloma_schedule_groups')

        # Deleting model 'Message'
        db.delete_table('paloma_message')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'paloma.alias': {
            'Meta': {'object_name': 'Alias'},
            'address': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'goto': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maildir': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {})
        },
        'paloma.domain': {
            'Meta': {'object_name': 'Domain'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'backupmx': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'domain': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maxquota': ('django.db.models.fields.BigIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'quota': ('django.db.models.fields.BigIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'transport': ('django.db.models.fields.CharField', [], {'max_length': '765'})
        },
        'paloma.group': {
            'Meta': {'unique_together': "(('owner', 'name'), ('owner', 'symbol'))", 'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['paloma.Owner']"}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        'paloma.mailbox': {
            'Meta': {'object_name': 'Mailbox'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'bounces': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['paloma.Group']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'paloma.message': {
            'Meta': {'object_name': 'Message'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailbox': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['paloma.Mailbox']"}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['paloma.Schedule']"}),
            'text': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'paloma.owner': {
            'Meta': {'object_name': 'Owner'},
            'domain': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'forward_to': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'paloma.schedule': {
            'Meta': {'object_name': 'Schedule'},
            'dt_start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'forward_to': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['paloma.Group']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['paloma.Owner']"}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '101'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['paloma']
