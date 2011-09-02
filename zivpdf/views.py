#coding: utf8

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db import connections
from django.utils.encoding import *


from django import http
from django.template.loader import get_template
from django.template import Context
import ho.pisa as pisa
import cStringIO as StringIO
import cgi




def write_pdf(template_src, context_dict):
  template = get_template(template_src)
  context = Context(context_dict)
  html  = template.render(context)
  result = StringIO.StringIO()
  pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
  if not pdf.err:
    return http.HttpResponse(result.getvalue(), mimetype='application/pdf')
  return http.HttpResponse('Gremlinsss ate your pdf! %s' % cgi.escape(html))


def get_cvs(request):
  cursor = connections['jobfair'].cursor()
  cursor.execute("SET NAMES 'utf8' COLLATE 'utf8_unicode_ci'")
  cursor.execute("SELECT firstname, lastname, adrp, adrb, email, web, byear, tel, mob, faculty, courseyear, highschool, activities, extras, languages, skills, workexp, about, expgrad, prefs, expectations FROM cvs where id=40")
  #return render_to_response('zivpdf.html', {'cvs' : cursor.fetchall(), 'labels': labele})
  return write_pdf('zivpdf.html',{
	'pagesize' : 'A4',
	'cvs' : cursor.fetchall()})
  

