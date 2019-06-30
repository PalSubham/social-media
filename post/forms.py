from django import forms
from .models import *

# Forms are here

class PostForm(forms.ModelForm):

    post_images = forms.ImageField(
        required = False,
        widget = forms.ClearableFileInput(attrs = {'multiple': True,})
    )

    class Meta:
        model = Post
        fields = ('heading', 'post_text', 'post_images', 'owner',)

        widgets = {
            'owner': forms.HiddenInput,
        }

        error_messages = {
            'heading': {
                'required': 'Please provide a heading.',
            },
        }