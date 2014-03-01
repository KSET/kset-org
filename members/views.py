#coding: utf8
import hashlib

from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *
from .decorators import require_auth


def _display_member(request, template, member):

    return render(request, template, {
        'member': member,
        'addresses': Address.objects.filter(member=member.id),
        'contacts': Contact.objects.filter(member=member.id),
        'groups': MemberGroupLink.objects.filter(member=member.id).order_by('date_start'),
    })


@require_auth
def index(request):
    member = get_object_or_404(Member, id=request.session.get('members_user_id'))
    return _display_member(request, 'main.html', member)


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


@require_auth
def get_member(request, id):
    try:
        member = Member.objects.get(id=id)
    except:
        raise Http404
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
