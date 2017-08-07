from django.contrib.admin import SimpleListFilter
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.translation import ugettext as _
from django.conf import settings


def send_template_email(
        member_email,
        member_name,
        reset_password_link,
        template='members_templates/emails/forgot_password_email.html',
        subject=_('kset.org: Reset Lozinke')):

    email_template = render_to_string(
        template,
        {
            'member_name': member_name,
            'reset_password_link': reset_password_link,
        })

    msg = EmailMessage(
        subject,
        email_template,
        settings.DEFAULT_FROM_EMAIL,
        [member_email])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send(fail_silently=True)


class MemberActiveFilter(SimpleListFilter):
    title = 'Aktivan'
    parameter_name = 'active'

    def lookups(self, request, model_admin):
        return [(True, 'Aktivan'), (False, 'Nije aktivan')]

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(leave_date__isnull=(self.value() == 'True'))
