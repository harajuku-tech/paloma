# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Enroll'
        db.create_table('paloma_enroll', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mailbox', self.gf('django.db.models.fields.related.OneToOneField')(default=None, to=orm['paloma.Mailbox'], unique=True, null=True, blank=True)),
            ('inviter', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['auth.User'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('prospect', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True, blank=True)),
            ('secret', self.gf('django.db.models.fields.CharField')(default='mCZhqQSOSchtugMqjGqJWbkltxt72dBy', unique=True, max_length=100)),
            ('short_secret', self.gf('django.db.models.fields.CharField')(default='qqqKwcat', unique=True, max_length=10)),
            ('dt_expire', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('dt_try', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('dt_commit', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal('paloma', ['Enroll'])

#        # Deleting field 'Mailbox.dt_secret'
#        db.delete_column('paloma_mailbox', 'dt_secret')

#        # Deleting field 'Mailbox.dt_try'
#        db.delete_column('paloma_mailbox', 'dt_try')
#
#        # Deleting field 'Mailbox.dt_commit'
#        db.delete_column('paloma_mailbox', 'dt_commit')
#
#        # Deleting field 'Mailbox.secret'
#        db.delete_column('paloma_mailbox', 'secret')

        # Adding unique constraint on 'Mailbox', fields ['address']
        db.create_unique('paloma_mailbox', ['address'])


    def backwards(self, orm):
        # Removing unique constraint on 'Mailbox', fields ['address']
        db.delete_unique('paloma_mailbox', ['address'])

        # Deleting model 'Enroll'
        db.delete_table('paloma_enroll')

        # Adding field 'Mailbox.dt_secret'
        db.add_column('paloma_mailbox', 'dt_secret',
                      self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Mailbox.dt_try'
        db.add_column('paloma_mailbox', 'dt_try',
                      self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Mailbox.dt_commit'
        db.add_column('paloma_mailbox', 'dt_commit',
                      self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Mailbox.secret'
        db.add_column('paloma_mailbox', 'secret',
                      self.gf('django.db.models.fields.CharField')(default='uAf5nC9kXAdDU2FFe7LB5SXWBHHWxB4I', max_length=100),
                      keep_default=False)


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
            'alias': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailbox': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
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
        'paloma.enroll': {
            'Meta': {'object_name': 'Enroll'},
            'dt_commit': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'dt_expire': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'dt_try': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inviter': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['auth.User']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'mailbox': ('django.db.models.fields.related.OneToOneField', [], {'default': 'None', 'to': "orm['paloma.Mailbox']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'prospect': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'default': "'aOo9yz07u4jyVVOvTlIIFk6Hf9FLFXX0'", 'unique': 'True', 'max_length': '100'}),
            'short_secret': ('django.db.models.fields.CharField', [], {'default': "'T0jfsG6d'", 'unique': 'True', 'max_length': '10'})
        },
        'paloma.group': {
            'Meta': {'unique_together': "(('owner', 'name'), ('owner', 'symbol'))", 'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['paloma.Owner']"}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        'paloma.journal': {
            'Meta': {'object_name': 'Journal'},
            'dt_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_jailed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'recipient': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'text': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'paloma.mailbox': {
            'Meta': {'object_name': 'Mailbox'},
            'address': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'bounces': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['paloma.Group']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'paloma.message': {
            'Meta': {'object_name': 'Message'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailbox': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['paloma.Mailbox']"}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['paloma.Schedule']"}),
            'text': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'paloma.operator': {
            'Meta': {'object_name': 'Operator'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['paloma.Owner']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
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
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '24', 'db_index': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '101'}),
            'task': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['paloma']
