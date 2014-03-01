# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'News'
        db.create_table(u'news_news', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=192)),
            ('description', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('content', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('expire_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('sticky', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('thumb', self.gf('filebrowser.fields.FileBrowseField')(max_length=255, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=128, blank=True)),
        ))
        db.send_create_signal(u'news', ['News'])


    def backwards(self, orm):
        # Deleting model 'News'
        db.delete_table(u'news_news')


    models = {
        u'news.news': {
            'Meta': {'object_name': 'News'},
            'content': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'expire_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128', 'blank': 'True'}),
            'sticky': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '192'}),
            'thumb': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['news']