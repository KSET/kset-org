# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'subpages_category')

        # Deleting model 'Subpage'
        db.delete_table(u'subpages_subpage')


    def backwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'subpages_category', (
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['subpages.Category'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'subpages', ['Category'])

        # Adding model 'Subpage'
        db.create_table(u'subpages_subpage', (
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['subpages.Category'], null=True, blank=True)),
            ('content', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('thumb', self.gf('filebrowser.fields.FileBrowseField')(max_length=255, null=True, blank=True)),
            ('description', self.gf('tinymce.models.HTMLField')(blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_edit', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal(u'subpages', ['Subpage'])


    models = {
        
    }

    complete_apps = ['subpages']