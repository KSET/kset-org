from django.contrib import admin
from events.models import Event


from django import forms
from django.core.urlresolvers import reverse
from tinymce.widgets import TinyMCE
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage

def make_announced(modeladmin, request, queryset):
  queryset.update(announce=True)

make_announced.short_description = "Najavi dogadaje"


class EventAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'date', 'time', 'announce', 'thumb', 'tags', 'price', 'description', 'content')
    list_display = ('title', 'date', 'announce', 'tags','slug',)
    ordering = ('-date',)
    search_fields = ('title', 'date', 'description', 'content')
    list_filter = ['tags']
    prepopulated_fields = {'slug': ('date','title',)}
    actions = [make_announced]

    class Media:
        js = (
            '/media/static/tiny_mce/tiny_mce.js',
            )



## mod flatpages
class TinyMCEFlatPageAdmin(FlatPageAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'content':
            return forms.CharField(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
                mce_attrs={'external_link_list_url': reverse('tinymce.views.flatpages_link_list')},
            ))
        return super(TinyMCEFlatPageAdmin, self).formfield_for_dbfield(db_field, **kwargs)

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, TinyMCEFlatPageAdmin)

admin.site.register(Event, EventAdmin)
