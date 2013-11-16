from django.contrib import admin

from .models import Subpage, Category


class SubpageAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'category', 'thumb', 'description', 'content')
    list_display = ('title', 'slug', 'category', 'last_edit')
    ordering = ('category', 'title',)
    search_fields = ('title', 'description')
    list_filter = ['category']

    class Media:
        js = (
            '/static/tiny_mce/tiny_mce.js',
        )


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Subpage, SubpageAdmin)
admin.site.register(Category, CategoryAdmin)
