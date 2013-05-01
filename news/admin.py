from django.contrib import admin

from .models import News


class NewsAdmin(admin.ModelAdmin):
    fields = ('subject', 'slug', 'sticky', 'expire_at', 'thumb', 'description', 'content')
    list_display = ('subject', 'created_at', 'expire_at')
    ordering = ('-created_at',)
    search_fields = ('subject', 'created_at')
    prepopulated_fields = {'slug': ('subject',)}

admin.site.register(News, NewsAdmin)
