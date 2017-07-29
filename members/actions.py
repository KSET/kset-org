#coding: utf-8

import unicodecsv
from .membership import InvoiceTemplate
from django.http import HttpResponse
from django.conf import settings
from django.utils.encoding import smart_str
import os


def export_as_csv_action(description="Izvoz odabranih stavki u CSV",
                         fields=None, exclude=None, header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """
    def export_as_csv(modeladmin, request, queryset):

        opts = modeladmin.model._meta

        if not fields:
            field_names = [field.name for field in opts.fields]
        else:
            field_names = fields

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')

        writer = unicodecsv.writer(response, encoding='utf-8')
        if header:
            writer.writerow(field_names)
        for obj in queryset:
            row = [__get_field(obj, field)() if callable(__get_field(obj, field)) else __get_field(obj, field) for field in field_names]
            writer.writerow(row)
        return response
    export_as_csv.short_description = description
    return export_as_csv


def make_bill(modeladmin, request, queryset):
    """Creates bill (.pdf) with memberships"""

    bill = InvoiceTemplate(os.path.join(settings.MEDIA_ROOT, 'uploads', 'invoice.pdf'))

    odd = True
    cnt = 437
    for member in queryset:
        bill.buyer['name'] = smart_str(member.name + " " + member.surname)
        bill.buyer['taxnum'] = member.id

        bill.info['num'] = "2011-" + str(cnt)
        bill.info['date'] = "04.01.2011."
        bill.info['items'] = [['članarina za SSFER', 100.0]]

        bill.populate()

        cnt = cnt + 1

        bill.newPage()

    bill.create()

make_bill.short_description = "Ispisi clanarine"


def __get_field(instance, field):
    field_path = field.split('.')
    attr = instance
    for elem in field_path:
        try:
            attr = getattr(attr, elem)
        except AttributeError:
            return None
    return attr
