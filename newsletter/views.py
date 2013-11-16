#coding: utf8

from django.http import HttpResponse
from django.views.decorators.http import require_POST

from .forms import SubscriptionForm


@require_POST
def subscribe(request):
    form = SubscriptionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponse('Uspješno ste se pretplatili!')
    else:
        return HttpResponse(
            form.errors.get('email', 'Oops! Something went wrong.'),
            status=400)
