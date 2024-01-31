from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegister(UserCreationForm):
    username = forms.CharField(max_length=30, help_text='Required. 30')
    email = forms.EmailField(max_length=254, help_text='Required. 254')
    first_name=forms.CharField(max_length=30, help_text='Required. 30')
    last_name=forms.CharField(max_length=30, help_text='Required. 30')
    password1=forms.CharField(widget=forms.PasswordInput, help_text='Required. 8')
    password2=forms.CharField(widget=forms.PasswordInput, help_text='Required. 8')

    class Meta:
        model= User
        fields=('username', 'email', 'password1', 'password2','first_name','last_name')

