from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import *

# Create your views here.

class SigninView(LoginView):
    form_class = SigninForm
    template_name = 'registration/signin.html'


class SignupView(FormView):
    model = User
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = '/'

    def form_valid(self, form):
        newuser = form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(request = self.request, username = username, password = password)

        if not user == None:
            userprofile = user.userprofile
            userprofile.timezone = form.cleaned_data.get('timezone')
            userprofile.birthday = form.cleaned_data.get('birthday')
            userprofile.save()
            login(self.request, user)
        else:
            newuser.delete()

        return super(SignupView, self).form_valid(form)
