
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect

from sajax import register
from .form import SignupForm


@sensitive_post_parameters()
@csrf_protect
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


@register
def signup(request, first_name, last_name, **kwargs):
    form = SignupForm(data=kwargs)
    response = {'is_success': True}
    if form.is_valid():
        form.save()
    else:
        response['is_success'] = False
        if '__all__' in form.errors:
            form.errors['password1'] = form.errors.pop('__all__')
        response['errors'] = form.errors
    return response


@sensitive_post_parameters()
@csrf_protect
@login_required
@register
def change_password(request, **kwargs):
    form = PasswordChangeForm(user=request.user, data=kwargs)
    if form.is_valid():
        form.save()
