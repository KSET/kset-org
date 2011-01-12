#coding: utf8 

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db.models import Q
from django.template import RequestContext

from news.models import News
from events.models import Event


def search(request):
    """Returns results of search query on news & events."""

    # quick fix! 
    error_msg = "Neispravan unos! (za pretragu su potrebna minimalno 3 znaka!)"

    response_dict = {}

    # check if query exists and its length
    #if 'query' in request.GET and len(request.GET['query']) >= 3 and len(request.GET['query']) <= 32:
    if 'query' in request.GET and 3 <= len(request.GET['query']) <= 32:

       # search titles -> chain words in query
        query_news = Q()
        query_events = Q()
        
        # append every word to chain
        for word in request.GET['query'].split():

            # exclude words with 1 or 2 characters
            if len(word) >= 3:
                query_news &= Q(subject__icontains=word) | Q(description__icontains=word) | Q(content__icontains=word)
                query_events &= Q(title__icontains=word) | Q(description__icontains=word) | Q(content__icontains=word)
            
        # fetch data
        response_dict['news'] =  News.objects.filter(query_news).order_by('-publish')
        response_dict['events'] = Event.objects.filter(query_events).order_by('-date')

    else:
        response_dict['error_msg'] = "Neispravan unos! (za pretragu su potrebna minimalno 3 znaka!)"


    # return results
    return render_to_response('search.html', 
            response_dict,
            context_instance=RequestContext(request))
    
 
