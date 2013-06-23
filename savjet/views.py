from savjet.models import Dezurstva
from django.shortcuts import render


def list_attendance(request):
    attendance = Dezurstva.objects.all()
    return render(request, 'dezurstva.html', {'attendance': attendance})
