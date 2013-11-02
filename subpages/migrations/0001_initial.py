# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'subpages_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['subpages.Category'], null=True, blank=True)),
        ))
        db.send_create_signal(u'subpages', ['Category'])

        # Adding model 'Subpage'
        db.create_table(u'subpages_subpage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('last_edit', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('description', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('content', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('thumb', self.gf('filebrowser.fields.FileBrowseField')(max_length=255, null=True, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['subpages.Category'], null=True, blank=True)),
        ))
        db.send_create_signal(u'subpages', ['Subpage'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'subpages_category')

        # Deleting model 'Subpage'
        db.delete_table(u'subpages_subpage')


    models = {
        u'subpages.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['subpages.Category']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'subpages.subpage': {
            'Meta': {'object_name': 'Subpage'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['subpages.Category']", 'null': 'True', 'blank': 'True'}),
            'content': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'description': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_edit': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'thumb': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['subpages']