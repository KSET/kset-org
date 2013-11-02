from django.shortcuts import render

from .models import Dezurstva


def list_attendance(request):
    attendance = Dezurstva.objects.all()
    return render(request, 'dezurstva.html', {'attendance': attendance})
