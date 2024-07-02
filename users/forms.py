from django import forms

from .models import User

class RegisterForm(forms.Form):

    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 != password2:
            self.add_error("password2", "Passwords did't match")


    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            self.add_error("email", "Current email already registered")

        return email


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())