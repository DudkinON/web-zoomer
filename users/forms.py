
from django import forms
from users.models import User


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=32,
                                       widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']
