
from sajax import register
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout


@register
def login(request, **kwargs):
    """
    Authenticates a user
    @param username
    @param password
    """
    user = authenticate(**kwargs)
    if user:
        auth_login(request, user)
    return bool(user)


@register
def logout(request):
    """
    Logs out a user
    """
    return auth_logout(request)
