# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Photographer'
        db.create_table(u'gallery_photographer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=255)),
        ))
        db.send_create_signal(u'gallery', ['Photographer'])

        # Adding model 'Album'
        db.create_table(u'gallery_album', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('upload_path', self.gf('filebrowser.fields.FileBrowseField')(max_length=255, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('description', self.gf('tinymce.models.HTMLField')(max_length=255)),
            ('date_of_event', self.gf('django.db.models.fields.DateField')()),
            ('date_of_upload', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('photographer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gallery.Photographer'], null=True)),
            ('initial', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('thumb', self.gf('filebrowser.fields.FileBrowseField')(max_length=255)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal(u'gallery', ['Album'])

        # Adding model 'Image'
        db.create_table(u'gallery_image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('caption', self.gf('tinymce.models.HTMLField')(max_length=255, null=True, blank=True)),
            ('photographer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gallery.Photographer'], null=True)),
            ('date_of_event', self.gf('django.db.models.fields.DateField')()),
            ('date_of_upload', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('upload_path', self.gf('filebrowser.fields.FileBrowseField')(max_length=255)),
        ))
        db.send_create_signal(u'gallery', ['Image'])

        # Adding M2M table for field album on 'Image'
        m2m_table_name = db.shorten_name(u'gallery_image_album')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('image', models.ForeignKey(orm[u'gallery.image'], null=False)),
            ('album', models.ForeignKey(orm[u'gallery.album'], null=False))
        ))
        db.create_unique(m2m_table_name, ['image_id', 'album_id'])


    def backwards(self, orm):
        # Deleting model 'Photographer'
        db.delete_table(u'gallery_photographer')

        # Deleting model 'Album'
        db.delete_table(u'gallery_album')

        # Deleting model 'Image'
        db.delete_table(u'gallery_image')

        # Removing M2M table for field album on 'Image'
        db.delete_table(db.shorten_name(u'gallery_image_album'))


    models = {
        u'gallery.album': {
            'Meta': {'object_name': 'Album'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'date_of_event': ('django.db.models.fields.DateField', [], {}),
            'date_of_upload': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('tinymce.models.HTMLField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'photographer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gallery.Photographer']", 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'thumb': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'upload_path': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'gallery.image': {
            'Meta': {'object_name': 'Image'},
            'album': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'images'", 'symmetrical': 'False', 'to': u"orm['gallery.Album']"}),
            'caption': ('tinymce.models.HTMLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'date_of_event': ('django.db.models.fields.DateField', [], {}),
            'date_of_upload': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photographer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gallery.Photographer']", 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'upload_path': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255'})
        },
        u'gallery.photographer': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Photographer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['gallery']