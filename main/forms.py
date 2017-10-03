from django import forms
from .models import Message


class ContactForm(forms.Form):
    username = forms.CharField(max_length=64)
    title = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=40)
    text = forms.CharField(max_length=250)

    class Meta:
        model = Message
        fields = ['email', 'username', 'title', 'text']
