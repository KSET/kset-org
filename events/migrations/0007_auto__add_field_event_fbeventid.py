# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Event.fbeventid'
        db.add_column(u'events_event', 'fbeventid',
                      self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Event.fbeventid'
        db.delete_column(u'events_event', 'fbeventid')


    models = {
        u'events.event': {
            'Meta': {'object_name': 'Event'},
            'announce': ('django.db.models.fields.BooleanField', [], {}),
            'content': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'daytime': ('django.db.models.fields.BooleanField', [], {}),
            'description': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'fbeventid': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128', 'blank': 'True'}),
            'tags': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'dbtype': "'text'", 'null': 'True', 'blank': 'True'}),
            'thumb': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '192'})
        }
    }

    complete_apps = ['events']