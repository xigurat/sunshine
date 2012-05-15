
from django.views.generic import TemplateView
#~ from django.contrib.auth.forms import UserCreationForm


class Home(TemplateView):
    template_name = 'sunshine/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Home, self).get_context_data(*args, **kwargs)
        #~ a = UserCreationForm()
        #~ context.update({
            #~ 'signup_form': a,
        #~ })
        return context
