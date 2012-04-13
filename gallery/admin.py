from django.contrib import admin
from gallery.models import *
from guardian.admin import GuardedModelAdmin
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from guardian.shortcuts import get_perms
from django.contrib.sites.models import Site
from guardian.shortcuts import get_objects_for_user
from guardian.core import ObjectPermissionChecker
from django.contrib.admin.util import unquote
from django.contrib.admin import *

class ImageAdmin(GuardedModelAdmin):
    fields = ('title', 'date_of_event', 'slug', 'caption', 'photographer', 'album', 'upload_path')
    prepopulated_fields = {'slug': ('date_of_event', 'title',)}
    list_display = ('title', 'photographer', 'caption', 'date_of_event', 'photographer')
    ordering = ('-date_of_upload',)
    search_fields = ('title', 'date_of_event', 'caption', 'photographer')

    class Media:
        js = (
            '/media/static/tiny_mce/tiny_mce.js',
            )


class AlbumAdmin(GuardedModelAdmin):
    fields = ('title', 'date_of_event', 'slug', 'upload_path', 'description', 'photographer', 'thumb','category')
    prepopulated_fields = {'slug': ('date_of_event','title',)}
    list_display = ('title', 'photographer', 'date_of_event','category')
    ordering = ('-date_of_upload',)
    search_fields = ('title','date_of_event','description')


#    def change_view(self, request, object_id, extra_context=None):
#      joe = User.objects.get(username=request.user)
#      obj = self.get_object(request, unquote(object_id))
#      site = Site.objects.get_current()
#      if (joe.has_perm("change_album", obj)):
#        #messages.add_message(request, messages.ERROR, u"You don't have the necessary permissions!")
#        #return HttpResponse(request.path)
#        return super(AlbumAdmin, self).change_view(request, object_id, extra_context=None)
#      else:
#        self.message_user(request, "Nemate ovlasti za editiranje ovog albuma!")
#        return HttpResponseRedirect("/admin/gallery/album/")
#
#    #TODO - delete_view
#
#    def queryset(self, request):
#      """
#      Filter the objects displayed in the change_list to only
#      display those for the currently signed in user.
#      """
#      qs = super(AlbumAdmin, self).queryset(request)
#      if request.user.is_superuser:
#        return qs
#      else:
#        #return qs.filter(owner=request.user)
#        qs = get_objects_for_user(request.user, 'view_album', Album.objects.all())
#        return qs



    class Media:
        js = (
            '/media/static/tiny_mce/tiny_mce.js',
            )


class PhotographerAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)
    ordering = ('-name',)
    search_fields = ('name',)
    



admin.site.register(Image, ImageAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Photographer, PhotographerAdmin)

