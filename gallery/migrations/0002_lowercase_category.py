# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Just converts category names to lowercase."
        orm.Album.objects.filter(category='LIVE').update(category='live')
        orm.Album.objects.filter(category='FOTO').update(category='foto')
        orm.Album.objects.filter(category='SCLIVE').update(category='sclive')

    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")

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
    symmetrical = True
