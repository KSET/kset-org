from django.contrib import admin
from news.models import News

class NewsAdmin(admin.ModelAdmin):
    fields = ('subject', 'slug', 'publish', 'expire', 'thumb', 'description', 'content')
    list_display = ('subject', 'publish', 'expire')
    ordering = ('-publish',)
    search_fields = ('subject', 'publish')
    prepopulated_fields = {'slug': ('subject',)}

    class Media:
        js = (
            '/media/static/tiny_mce/tiny_mce.js',
            )

admin.site.register(News, NewsAdmin)
