# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        """
        We go through all events and take the tags Charfield, split it based on ','
        strip of whitespace, remove empty strings and assign that to tags_arr
        which is a pg array type
        """
        events = orm.Event.objects.all()
        for event in events:
            tags = filter(
                lambda tag: bool(tag),
                map(lambda tag: tag.strip(), event.tags.split(','))
            )
            event.tags_arr = tags
            event.save()

    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")

    models = {
        u'events.event': {
            'Meta': {'object_name': 'Event'},
            'announce': ('django.db.models.fields.BooleanField', [], {}),
            'content': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'daytime': ('django.db.models.fields.BooleanField', [], {}),
            'description': ('tinymce.models.HTMLField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128', 'blank': 'True'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'tags_arr': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'dbtype': "'text'", 'null': 'True', 'blank': 'True'}),
            'thumb': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '192'})
        }
    }

    complete_apps = ['events']
    symmetrical = True
