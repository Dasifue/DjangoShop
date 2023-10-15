from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError

from ..account.models import User

from ..account.utils import slugify
from django.contrib.auth import authenticate

class RegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField()
    password_confirm = serializers.CharField()

    class Meta:
        model = User
        fields = ("username", "email", "password", "password_confirm")

    def validate_password(self, password):
        if len(password) < 8:
            raise ValidationError("Password must contain at least 8 elements!")
        elif password.isdigit() or password.isalpha() or password.isspace() or password.islower() or password.isupper():
            raise ValidationError("Password is too easy!")
        return password
        

    def validate(self, attrs):
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")
        if password != password_confirm:
            raise ValidationError({"password": "Passwords don't match!"})
        return super().validate(attrs)
    

    def create(self, validated_data):
        while True:
            try:
                user = User.objects.create(
                    slug = slugify(value=validated_data.get("username")),
                    username = validated_data.get("username"),
                    email = validated_data.get("email"),
                )
                user.set_password(raw_password=validated_data.get("password"))
                user.save()
            except IntegrityError:
                continue
            else:
                break
        return user
    

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
        )


class ResetPasswordSerializer(serializers.ModelSerializer):

    new_password = serializers.CharField()

    class Meta:
        model = User
        fields = ("password", "new_password")

    def validate_new_password(self, password):
        if len(password) < 8:
            raise ValidationError("Password must contain at least 8 elements!")
        elif password.isdigit() or password.isalpha() or password.isspace() or password.islower() or password.isupper():
            raise ValidationError("Password is too easy!")
        return password

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get("new_password"))
        instance.save()
        return instance
