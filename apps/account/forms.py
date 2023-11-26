from typing import Any
from django import forms
from django.core.exceptions import ValidationError

from .models import User


class RegisterForm(forms.ModelForm):

    password = forms.CharField(max_length=20)
    password_confirm = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ("username", "email", "password", "password_confirm")

    def clean(self) -> dict[str, Any]:
        password: str = self.cleaned_data.get("password")
        password_confirm: str = self.cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise ValidationError({"password": "Passwords didn't match!"})
        
        return super().clean()
    
    def clean_password(self):
        password: str = self.cleaned_data.get("password")
        
        if len(password) < 8:
            raise ValidationError("Password must contain minimum 8 elements!")
        elif password.isdigit() or password.isalpha() or password.isspace() or password.islower() or password.isupper():
            raise ValidationError("Password is too easy!")
        return password
    
    

class LoginForm(forms.Form):
    password = forms.CharField(max_length=20)
    username = forms.CharField(max_length=30)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "avatar",
            "phone",
            "address",
            "country",
            "city",
            "zip",
        )

    def clean_first_name(self):
        first_name: str = self.cleaned_data["first_name"]

        if not first_name.isalpha():
            raise ValidationError(message="First name must contain only letters!")

        return first_name
    

    def clean_last_name(self):
        last_name: str = self.cleaned_data["last_name"]

        if not last_name.isalpha():
            raise ValidationError(message="Last name must contain only letters!")

        return last_name
    

    def clean_phone(self):
        phone: str = self.cleaned_data["phone"]

        if not phone.isascii():
            raise ValidationError("Not allowed simbols!")
        
        for letter in phone:
            if letter.isalpha():
                raise ValidationError("Not allowed simbols!")
        
        return phone
    

    def clean_zip(self):
        zip: str = self.cleaned_data["zip"]

        if not zip.isdigit():
            raise ValidationError(message="ZIP code must contain only numbers!")

        return zip




class ResetPasswordForm(forms.ModelForm):

    new_password = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = (
            "password",
            "new_password",
        )

    def clean_new_password(self):
        password: str = self.cleaned_data.get("new_password")
        
        if len(password) < 8:
            raise ValidationError("Password must contain minimum 8 elements!")
        elif password.isdigit() or password.isalpha() or password.isspace() or password.islower() or password.isupper():
            raise ValidationError("Password is too easy!")
        return password