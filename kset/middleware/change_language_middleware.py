from django.utils import translation
from django.http import HttpResponseRedirect


class ChangeLanguageMiddleware(object):
    """
    If get param "lang" is present, it will activate language set in param.
    After setting language, redirect to requested path will be made to remove lang param
    """
    def process_request(self, request):
        if 'lang' in request.GET:
            request.session['django_language'] = request.GET['lang'].lower()
            translation.activate(request.GET['lang'].lower())
            return HttpResponseRedirect(request.path)

