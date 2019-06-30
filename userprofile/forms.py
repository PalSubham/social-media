from django import forms
from django.contrib.auth import authenticate, forms as auth_forms
from django.contrib.auth.models import User

# Forms are here

class SigninForm(auth_forms.AuthenticationForm):
    
    email_id = forms.EmailField(
        widget = forms.EmailInput,
        error_messages = {
            'required': 'Please enter your email id.',
        }
    )

    field_order = ('username', 'password', 'email_id',)

    def __init__(self, request = None, *args, **kwargs):
        super(SigninForm, self).__init__(request, *args, **kwargs)

        self.fields['username'].error_messages['required'] = 'Please enter your username.'
        self.fields['password'].error_messages['required'] = 'Please enter your password'

        return

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

    birthday = forms.DateField(
        widget = forms.DateInput,
        error_messages = {
            'required': 'Please enter your birthdate.',
        }
    )

    timezone = forms.CharField(widget = forms.HiddenInput)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'birthday', 'password1', 'password2', 'timezone',)

        widgets = {
            'username': forms.TextInput,
            'first_name': forms.TextInput,
            'last_name': forms.TextInput,
            'email': forms.EmailInput,
        }

        error_messages = {
            'username': {
                'required': 'Please enter your username.',
                'invalid': 'Invalid username. Follow the given format',
            },
            'password1': {
                'required': 'Please enter your password.',
            },
            'password2': {
                'required': 'Please reenter your password for confirmation.',
            },
            'first_name': {
                'required': 'Please enter your first name.',
            },
            'last_name': {
                'required': 'Please enter your last name.',
            },
            'email': {
                'required': 'Please enter your email id.',
            },
        }
