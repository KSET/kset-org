#coding: utf8

from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .forms import SubscriptionForm


@require_POST
@csrf_exempt
def subscribe(request):
    form = SubscriptionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponse('Uspješno ste se pretplatili!')
    else:
        return HttpResponse(form.errors.values())
