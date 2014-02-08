from django.contrib import admin

from .models import Album, Image, Photographer


class ImageAdmin(admin.ModelAdmin):
    fields = ('title', 'date_of_event', 'slug', 'caption', 'photographer',
        'album', 'upload_path')
    prepopulated_fields = {'slug': ('date_of_event', 'title',)}
    list_display = ('title', 'photographer', 'caption', 'date_of_event',
        'photographer')
    ordering = ('-date_of_upload',)
    search_fields = ('title', 'date_of_event', 'caption')


class AlbumAdmin(admin.ModelAdmin):
    fields = ('title', 'date_of_event', 'slug', 'upload_path', 'description',
        'photographer', 'thumb', 'category')
    prepopulated_fields = {'slug': ('date_of_event', 'title',)}
    list_display = ('title', 'photographer', 'date_of_event', 'category')
    ordering = ('-date_of_upload',)
    search_fields = ('title', 'date_of_event', 'description')


class PhotographerAdmin(admin.ModelAdmin):
    fields = ('name', 'url',)
    list_display = ('name', 'url',)
    ordering = ('-name',)
    search_fields = ('name',)


admin.site.register(Image, ImageAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Photographer, PhotographerAdmin)
