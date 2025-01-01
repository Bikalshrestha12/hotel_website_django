from django import forms
from . models import *
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'email', "password1","password2"]

class ContactForm(forms.Form):
    full_name = forms.CharField()
    phone_no = forms.IntegerField()
    email = forms.EmailField()
    messages=forms.Textarea()
