# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Member'
        db.delete_table('paloma_member')

        # Removing M2M table for field groups on 'Member'
        db.delete_table('paloma_member_groups')

        # Adding model 'Optin'
        db.create_table('paloma_optin', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mailbox', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['paloma.Mailbox'])),
        ))
        db.send_create_signal('paloma', ['Optin'])

        # Adding M2M table for field groups on 'Optin'
        db.create_table('paloma_optin_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('optin', models.ForeignKey(orm['paloma.optin'], null=False)),
            ('group', models.ForeignKey(orm['paloma.group'], null=False))
        ))
        db.create_unique('paloma_optin_groups', ['optin_id', 'group_id'])

        # Adding model 'Mailbox'
        db.create_table('paloma_mailbox', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('bounces', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('paloma', ['Mailbox'])

        # Deleting field 'Message.member'
        db.delete_column('paloma_message', 'member_id')

        # Adding field 'Message.optin'
        db.add_column('paloma_message', 'optin', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['paloma.Optin']), keep_default=False)

        # Adding field 'Owner.forward_to'
        db.add_column('paloma_owner', 'forward_to', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding model 'Member'
        db.create_table('paloma_member', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('paloma', ['Member'])

        # Adding M2M table for field groups on 'Member'
        db.create_table('paloma_member_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('member', models.ForeignKey(orm['paloma.member'], null=False)),
            ('group', models.ForeignKey(orm['paloma.group'], null=False))
        ))
        db.create_unique('paloma_member_groups', ['member_id', 'group_id'])

        # Deleting model 'Optin'
        db.delete_table('paloma_optin')

        # Removing M2M table for field groups on 'Optin'
        db.delete_table('paloma_optin_groups')

        # Deleting model 'Mailbox'
        db.delete_table('paloma_mailbox')

        # Adding field 'Message.member'
        db.add_column('paloma_message', 'member', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['auth.User']), keep_default=False)

        # Deleting field 'Message.optin'
        db.delete_column('paloma_message', 'optin_id')

        # Deleting field 'Owner.forward_to'
        db.delete_column('paloma_owner', 'forward_to')


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
        'paloma.draft': {
            'Meta': {'object_name': 'Draft'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['paloma.Owner']"})
        },
        'paloma.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['paloma.Owner']"})
        },
        'paloma.mailbox': {
            'Meta': {'object_name': 'Mailbox'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'bounces': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'paloma.message': {
            'Meta': {'object_name': 'Message'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'optin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['paloma.Optin']"}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['paloma.Schedule']"}),
            'text': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        'paloma.optin': {
            'Meta': {'object_name': 'Optin'},
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['paloma.Group']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailbox': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['paloma.Mailbox']"})
        },
        'paloma.owner': {
            'Meta': {'object_name': 'Owner'},
            'forward_to': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'paloma.schedule': {
            'Meta': {'object_name': 'Schedule'},
            'draft': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['paloma.Draft']"}),
            'dt_start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'forward_to': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['paloma.Group']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['paloma']
