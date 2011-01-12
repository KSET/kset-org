#coding: utf8

from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, Template

from django.core.exceptions import ValidationError

from newsletter.models import Subscription


def subscribe(request):
    if 'subscription' in request.POST:
        subscription = Subscription(email = request.POST['subscription'])
        subscriptions = Subscription.objects.filter(email = request.POST['subscription'])

        try:
            subscription.full_clean()
            subscription.save()
            return HttpResponse('Uspješno ste se pretplatili!')
        except ValidationError, e:
            if (subscriptions.count() != 0):
              return HttpResponse('E-mail adresa je vec pretplacena!')
            else:
              return HttpResponse('Došlo je do pogreške!')
    else:
        return HttpRedirect('http://www.kset.org/');


### OLD

def list_subscriptions(request):
    subscriptions = Subscription.objects.all()
    return render_to_response('list.html', {'subs' : subscriptions})

#nema gumba jos
def unsubscribe(request):
	if 'subscription_email' in request.POST:
		subscription = Subscription.objects.filter(email = request.POST['subscription_email'])
		if subscription:
			subscription.delete()
			return HttpResponse('E-mail uspjesno obrisan!')
		else:
			return HttpResponse('Failed!')
 
