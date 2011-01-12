from django.contrib import admin
from savjet.models import *

class ZapisnikAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'author',)
    search_fields = ('title', 'content', )
    list_filter = ('author', 'date', )
    ordering = ('-date',)

    class Media:
            js = (
      'admin/tinymce/jscripts/tiny_mce/tiny_mce.js',
      'admin/tinymce_setup/tinymce_description.js',
      'admin/tinymce_setup/tinymce_content.js',
      )

admin.site.register(Zapisnik, ZapisnikAdmin)

