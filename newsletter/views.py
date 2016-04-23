#coding: utf-8

from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from .forms import SubscriptionForm
from django.shortcuts import render


def subscribe(request):
    if request.method == 'GET':
        return render(request, 'newsletter-form.html')

    form = SubscriptionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponse(_('newsletter.subscription.successful'))
    else:
        return HttpResponse(
            # Translators: 'Oops! Something went wrong.'
            form.errors.get('email', _('newsletter.subscription.error')),
            status=400)
