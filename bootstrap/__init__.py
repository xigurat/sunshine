
from django.template import loader, Context
from django.forms.forms import BaseForm


class BootstrapForm(object):
    def as_bootstrap(self):
        template = loader.get_template('bootstrap/form.html')
        context = Context({
            'form': self
        })
        return template.render(context)


BaseForm.__bases__ = (BootstrapForm,) + BaseForm.__bases__
