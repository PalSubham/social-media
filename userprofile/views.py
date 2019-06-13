from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login
from .forms import *
from .models import *

# Create your views here.

class SigninView(LoginView):
    form_class = SigninForm
    template_name = 'registration/signin.html'


class SignupView(FormView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username = username, password = password)
        user.first_name = form.cleaned_data.get('first_name')
        user.last_name = form.cleaned_data.get('last_name')
        user.email = form.cleaned_data.get('email_id')
        user.save()
        userprofile = UserProfile.objects.get(owner = user)
        userprofile.timezone = form.cleaned_data.get('timezone')
        userprofile.birthday = form.cleaned_data.get('birthday')
        userprofile.save()
        login(self.request, user)
        return redirect('root')
