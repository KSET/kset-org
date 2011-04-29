# Create your views here.
from savjet.models import Dezurstva
from django.shortcuts import render_to_response


def list_attendance(request):
  attendance = Dezurstva.objects.all()
  return render_to_response('dezurstva.html', {'attendance' : attendance})
