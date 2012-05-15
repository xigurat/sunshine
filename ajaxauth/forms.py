
from django import forms
from registration.forms import RegistrationForm
from django.utils.translation import ugettext_lazy as _


class SignupForm(RegistrationForm):
    first_name = forms.CharField(max_length=30, label=_('first name'))
    last_name = forms.CharField(max_length=30, label=_('last name'))

    def save(self):
        user = super(SignupForm, self).save()
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
