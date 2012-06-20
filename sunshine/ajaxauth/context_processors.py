
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from .forms import SignupForm


def ajaxauth(request):
    if request.user.is_authenticated():
        context = {
            'change_password_form': PasswordChangeForm(user=request.user),
        }
    else:
        context = {
            'login_form': AuthenticationForm(request),
            'signup_form': SignupForm()
        }
    return context
