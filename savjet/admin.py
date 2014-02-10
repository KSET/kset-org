from django.contrib import admin


from .models import *


class ZapisnikAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'author',)
    search_fields = ('title', 'content', )
    list_filter = ('author', 'date', )
    fields = ('date', 'title', 'content')
    ordering = ('-date',)

    def save_model(self, request, obj, form, change):
        """When creating a new object, set the author field."""
        if not change:
            obj.author = request.user
        obj.save()


class DezurstvaAdmin(admin.ModelAdmin):
    list_display = ('start', 'end', 'content',)

admin.site.register(Zapisnik, ZapisnikAdmin)
admin.site.register(Dezurstva, DezurstvaAdmin)
