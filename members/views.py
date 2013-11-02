#coding: utf8
import hashlib

from django.http import Http404
from django.shortcuts import render, redirect

from .forms import *
from .models import *


def require_auth(view):
    """Custom decorator, checks if user is logged in."""
    def wrapper(request, *args):

        if not request.session.get('user_id', False):
            return redirect('members-login')

        return view(request, *args)
    return wrapper


def get_current_user(request):
    """Gets Member object of currently logged in user."""
    user_id = request.session.get('user_id', False)

    return Member.objects.get(id=user_id)


def login(request):
    if request.session.get('user_id', False):
        return redirect('members')
    else:
        # check if form data is posted
        if (request.method == 'POST'):
            username = request.POST.get("username")
            password = request.POST.get("password")
            pwhash = hashlib.md5(password).hexdigest()
            # check username + password

            try:
                member = Member.objects.get(password=pwhash, username=username)

                request.session['user_id'] = member.id
                return redirect('members')
            except:
                return render(request, 'login.html', {'loginFailed': True})
        else:
            return render(request, 'login.html')


def logout(request):
    if request.session.get('user_id', False):
        request.session.flush()

    return redirect('members-login')


def display_member(request, template, member):
    if request.session.get('user_id', False) == member.id:
        isProfileOwner = True
    else:
        isProfileOwner = False

    return render(request, template, {
        'member': member,
        'addresses': Address.objects.filter(member=member.id),
        'contacts': Contact.objects.filter(member=member.id),
        'groups': MemberGroupLink.objects.filter(member=member.id),
        'isProfileOwner': isProfileOwner
    })


@require_auth
def main(request):
    member = get_current_user(request)
    return display_member(request, 'main.html', member)


@require_auth
def member(request, memberId):
    try:
        member = Member.objects.get(id=memberId)
    except:
        raise Http404
    return display_member(request, 'main.html', member)


@require_auth
def listAll(request):
    members = Member.objects.order_by('surname', 'name')
    return render(request, 'members-list.html', {
        'members': members})


@require_auth
def edit(request):
    member = get_current_user(request)
    return render(request, 'edit-profile.html', {
        'member': member,
        'addresses': Address.objects.filter(member=member.id),
        'contacts': Contact.objects.filter(member=member.id),
        'groups': MemberGroupLink.objects.filter(member=member.id),
        'contactTypes': ContactType.objects.all()
    })


@require_auth
def submit(request):
    member = get_current_user(request)
    addresses = Address.objects.filter(member=member.id)
    contacts = Contact.objects.filter(member=member.id)
    groups = MemberGroupLink.objects.filter(member=member.id)
    contactTypes = ContactType.objects.all()

    return render(request, 'edit-profile.html', {
        'member': member,
        'addresses': addresses,
        'contacts': contacts,
        'groups': groups,
        'contactTypes': contactTypes
    })


def red(request):
    """Print out in html red members addresses."""

    members = Member.objects.filter(groups__id=16).exclude(death__isnull=False).order_by('surname', 'name')

    for member in members:
        member.addresses = Address.objects.filter(member=member.id)

    return render(request, 'members-red.html', {
        'members': members,
    })


def red_list(request):
    """Print out in html red members addresses."""

    members = Member.objects.filter(groups__id=16).exclude(death__isnull=False).order_by('surname', 'name')

    return render(request, 'members-red-list.html', {
        'members': members,
    })
