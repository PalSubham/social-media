from django import forms
from django.contrib.auth import authenticate, forms as auth_forms
from django.contrib.auth.models import User

# Forms are here

class SigninForm(auth_forms.AuthenticationForm):

    username = auth_forms.UsernameField(widget = forms.TextInput)
    password = forms.CharField(strip = False, widget = forms.PasswordInput)
    email_id = forms.EmailField(widget = forms.EmailInput)

    def __init__(self, request = None, *args, **kwargs):
        super(SigninForm, self).__init__(request, *args, **kwargs)
        return

    class Meta:
        model = User
        fields = ('username', 'password', 'email_id',)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        email_id = self.cleaned_data.get('email_id')

        if username is not None and password and email_id:
            self.user_cache = authenticate(self.request, username = username, password = password)
            if not self.user_cache:
                raise forms.ValidationError("Username or Password is incorrect")
            if not self.user_cache.is_active:
                raise forms.ValidationError('This user is not active')
            if not self.user_cache.email == email_id:
                raise forms.ValidationError('Incorrect Email ID')
        
        return self.cleaned_data


class SignUpForm(auth_forms.UserCreationForm):

    first_name = forms.CharField(widget = forms.TextInput)
    last_name = forms.CharField(widget = forms.TextInput)
    email_id = forms.EmailField(widget = forms.EmailInput)
    birthday = forms.DateField(widget = forms.DateInput)
    timezone = forms.CharField(widget = forms.HiddenInput)
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        return
    
    class Meta:
        model = User
        fields = ('timezone', 'username', 'first_name', 'last_name', 'email_id', 'birthday', 'password1', 'password2',)

        widgets = {
            'username': forms.TextInput,
            'password1': forms.PasswordInput,
            'password2': forms.PasswordInput,
        }
