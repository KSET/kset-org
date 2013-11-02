# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Group'
        db.create_table(u'members_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.Group'], null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
        ))
        db.send_create_signal(u'members', ['Group'])

        # Adding model 'Member'
        db.create_table(u'members_member', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('card_id', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('birth', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('death', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('comment', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'members', ['Member'])

        # Adding model 'MemberGroupLink'
        db.create_table(u'members_membergrouplink', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.Member'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.Group'])),
            ('date_start', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date_end', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'members', ['MemberGroupLink'])

        # Adding model 'ContactType'
        db.create_table(u'members_contacttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'members', ['ContactType'])

        # Adding model 'Contact'
        db.create_table(u'members_contact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.Member'])),
            ('contact', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('contact_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.ContactType'])),
        ))
        db.send_create_signal(u'members', ['Contact'])

        # Adding model 'Address'
        db.create_table(u'members_address', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.Member'])),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('town', self.gf('django.db.models.fields.CharField')(default='Zagreb', max_length=32, null=True, blank=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(default='10000', max_length=16, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(default='Hrvatska', max_length=32, null=True, blank=True)),
        ))
        db.send_create_signal(u'members', ['Address'])


    def backwards(self, orm):
        # Deleting model 'Group'
        db.delete_table(u'members_group')

        # Deleting model 'Member'
        db.delete_table(u'members_member')

        # Deleting model 'MemberGroupLink'
        db.delete_table(u'members_membergrouplink')

        # Deleting model 'ContactType'
        db.delete_table(u'members_contacttype')

        # Deleting model 'Contact'
        db.delete_table(u'members_contact')

        # Deleting model 'Address'
        db.delete_table(u'members_address')


    models = {
        u'members.address': {
            'Meta': {'object_name': 'Address'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'Hrvatska'", 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.Member']"}),
            'town': ('django.db.models.fields.CharField', [], {'default': "'Zagreb'", 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'default': "'10000'", 'max_length': '16', 'null': 'True', 'blank': 'True'})
        },
        u'members.contact': {
            'Meta': {'object_name': 'Contact'},
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'contact_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.ContactType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.Member']"})
        },
        u'members.contacttype': {
            'Meta': {'object_name': 'ContactType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'members.group': {
            'Meta': {'object_name': 'Group'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.Group']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'members.member': {
            'Meta': {'object_name': 'Member'},
            'birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'card_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'comment': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'death': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['members.Group']", 'through': u"orm['members.MemberGroupLink']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        },
        u'members.membergrouplink': {
            'Meta': {'object_name': 'MemberGroupLink'},
            'date_end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.Member']"})
        }
    }

    complete_apps = ['members']