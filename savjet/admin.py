from django.contrib import admin


from .models import *


class ZapisnikAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'author',)
    search_fields = ('title', 'content', )
    list_filter = ('author', 'date', )
    ordering = ('-date',)

    class Media:
        js = (
            '/static/tiny_mce/tiny_mce.js',
        )


class DezurstvaAdmin(admin.ModelAdmin):
    list_display = ('start', 'end', 'content',)

    class Media:
        js = (
            '/static/tiny_mce/tiny_mce.js',
        )

admin.site.register(Zapisnik, ZapisnikAdmin)
admin.site.register(Dezurstva, DezurstvaAdmin)
