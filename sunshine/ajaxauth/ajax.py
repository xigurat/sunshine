
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.db import transaction

from sajax import register
from .forms import SignupForm


@sensitive_post_parameters()
@never_cache
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


@sensitive_post_parameters()
@transaction.commit_on_success
@register
def signup(request, **kwargs):
    """
    Signs up a user in the application
    @param username
    @param email
    @param password1
    @param password2
    @param first_name
    @param last_name
    """
    form = SignupForm(data=kwargs)
    return _save_form(form)


@sensitive_post_parameters()
@register
@login_required
def change_password(request, **kwargs):
    """
    Changes the user password
    """
    form = PasswordChangeForm(user=request.user, data=kwargs)
    return _save_form(form)


def _save_form(form):
    response = {'is_success': True}
    if form.is_valid():
        form.save()
    else:
        response['is_success'] = False
        response['errors'] = form.errors
    return response
