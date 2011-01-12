from django.contrib import admin
from events.models import Event

def make_announced(modeladmin, request, queryset):
  queryset.update(announce=True)

make_announced.short_description = "Najavi dogadaje"


class EventAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'date', 'time', 'announce', 'thumb', 'tags', 'price', 'description', 'content')
    list_display = ('title', 'date', 'announce', 'tags',)
    ordering = ('-date',)
    search_fields = ('title', 'date', 'description', 'content')
    list_filter = ['tags']
    prepopulated_fields = {'slug': ('date','title',)}
    actions = [make_announced]

    class Media:
        js = (
            'admin/tinymce/jscripts/tiny_mce/tiny_mce.js',
            'admin/tinymce_setup/tinymce_content.js',
            'admin/tinymce_setup/tinymce_description.js',
            )

admin.site.register(Event, EventAdmin)
