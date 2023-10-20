from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import IntegrityError

from .utils import slugify

class User(AbstractUser):
    slug = models.SlugField("Slug", max_length=100, unique=True, null=False)
    email = models.EmailField("Email", unique=True)
    avatar = models.ImageField("Avatar", upload_to="users/", default="default/default-avatar.png")

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.email}"
    
    @property
    def full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()
    

    def save(self, *args, **kwargs):
        while True:
            self.slug = slugify(value=self.username)
            try:
                return super().save(*args, **kwargs)
            except IntegrityError:
                continue
            
        