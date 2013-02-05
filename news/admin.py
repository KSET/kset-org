from django.contrib import admin
from news.models import News

class NewsAdmin(admin.ModelAdmin):
    fields = ('subject', 'slug', 'sticky', 'expire_at', 'thumb', 'description', 'content')
    list_display = ('subject', 'created_at', 'expire_at')
    ordering = ('-created_at',)
    search_fields = ('subject', 'created_at')
    prepopulated_fields = {'slug': ('subject',)}

    class Media:
        js = (
            '/media/static/tiny_mce/tiny_mce.js',
            )

admin.site.register(News, NewsAdmin)
