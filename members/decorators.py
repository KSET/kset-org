from django.shortcuts import redirect


def require_auth(view):
    """Custom decorator, checks if user is logged in."""
    def wrapper(request, *args, **kwargs):

        if not request.session.get('members_user_id'):
            return redirect('members_login')

        return view(request, *args, **kwargs)
    return wrapper
