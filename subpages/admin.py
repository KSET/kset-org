from django.contrib import admin
from subpages.models import Subpage, Category

class SubpageAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'category', 'thumb', 'description', 'content')
    list_display = ('title', 'slug', 'category', 'last_edit')
    ordering = ('category', 'title',)
    search_fields = ('title', 'description')
    list_filter = ['category']

    class Media:
        js = (
            'admin/tinymce/jscripts/tiny_mce/tiny_mce.js',
            'admin/tinymce_setup/tinymce_content.js',
            'admin/tinymce_setup/tinymce_description.js',
            )        

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Subpage, SubpageAdmin)
admin.site.register(Category, CategoryAdmin)
