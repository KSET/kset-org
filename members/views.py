#coding: utf8
import hashlib

from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from ajaxuploader.views import AjaxFileUploader
from ajaxuploader.backends.thumbnail import ThumbnailUploadBackend

from .forms import *
from .models import *
from .decorators import require_auth


import_uploader = AjaxFileUploader(backend=ThumbnailUploadBackend, DIMENSIONS="188", KEEP_ORIGINAL=False)


def _display_member(request, template, member, address_form=None, contact_form=None):

    return render(request, template, {
        'member': member,
        'is_owner': member.id == request.session['members_user_id'],
        'addresses': Address.objects.filter(member=member.id),
        'contacts': Contact.objects.filter(member=member.id),
        'groups': MemberGroupLink.objects.filter(member=member.id).order_by('date_start'),
        'address_form': address_form,
        'contact_form': contact_form
    })


@require_auth
def index(request):
    member = get_object_or_404(Member, id=request.session.get('members_user_id'))
    address = Address(member=member)
    contact = Contact(member=member)
    address_form = AddAddressForm(request.POST or None, instance=address)
    contact_form = AddContactForm(request.POST or None, instance=contact)
    if request.method == 'POST':
        if address_form.is_valid():
            address_form.save()
            return redirect('members_index')
        if contact_form.is_valid():
            contact_form.save()
            return redirect('members_index')
    return _display_member(request, 'main.html', member, address_form, contact_form)


@require_auth
@require_POST
def update_avatar(request):
    member = get_object_or_404(Member, id=request.session['members_user_id'])
    # FIXME: We should use a form here
    filename = request.POST.get('filename')
    if filename:
        member.image = filename
        member.save()
        return redirect('members_index')


def login(request):
    if request.session.get('members_user_id'):
        return redirect('members_index')
    form = LoginForm(request.POST or None)
    if form.is_valid():

        request.session['members_user_id'] = form.cleaned_data['member']
        request.session.save()
        return redirect('members_index')
    else:
        return render(request, 'login.html', {'form': form})


def logout(request):
    if request.session.get('members_user_id'):
        request.session['members_user_id'] = None

    return redirect('members_login')


def forgot_password(request):
    form = MemberForgotPasswordForm(request.POST or None)
    if form.is_valid():
        form.send_password_reset_email()
        messages.success(request, 'Uskoro ćete dobiti email sa uputama kako resetirati lozinku.')
        return redirect('members_login')
    return render(request, 'forgot_password.html', {'form': form})


def reset_password(request, link):
    try:
        rpl = ResetPasswordLink.objects.get(unique_link=link)
        if not rpl.is_still_valid():
            messages.error(request, 'Link za resetiranje passworda je istekao.')
            return redirect('members_login')
    except ResetPasswordLink.DoesNotExist:
        messages.error(request, 'Nije valjan link za reset lozinke.')
        return redirect('members_login')
    form = ResetPasswordForm(request.POST or None)
    if form.is_valid():
        form.set_new_password(rpl=rpl)
        messages.success(request, 'Uspješno ste resetirali lozinku. Sada se ulogirajte se.')
        return redirect('members_login')
    return render(request, 'reset_password.html', {'form': form})


@require_auth
def get_member(request, id):
    member = get_object_or_404(Member, id=id)
    return _display_member(request, 'main.html', member)


@require_auth
def list_all(request):
    members = Member.objects.order_by('surname', 'name')
    filter_form = MemberFilterForm(request.POST or None)
    if filter_form.is_valid():
        members = filter_form.filter()

    return render(request, 'members-list.html', {
        'members': members,
        'filter_form': filter_form})


@require_auth
@require_http_methods(["DELETE"])
def delete_address(request, id):
    member = get_object_or_404(Member, id=request.session['members_user_id'])
    address = get_object_or_404(Address, id=id)
    if member.id == address.memer_id:
        address.delete()
        return redirect('members_index')
    else:
        raise PermissionDenied()


@require_auth
@require_http_methods(["DELETE"])
def delete_contact(request, id):
    member = get_object_or_404(Member, id=request.session['members_user_id'])
    contact = get_object_or_404(contact, id=id)
    if member.id == contact.memer_id:
        contact.delete()
        return redirect('members_index')
    else:
        raise PermissionDenied()


@login_required
def red_table(request):
    """Print out in html red members addresses."""

    members = Member.objects.filter(
        groups__id=16).exclude(
        death__isnull=False).order_by('surname', 'name')

    for member in members:
        member.addresses = Address.objects.filter(member=member.id)

    return render(request, 'members-red.html', {
        'members': members,
    })


@login_required
def red_list(request):
    """Print out in html red members addresses."""

    members = Member.objects.filter(
        groups__id=16).exclude(
        death__isnull=False).order_by('surname', 'name')

    return render(request, 'members-red-list.html', {
        'members': members,
    })
