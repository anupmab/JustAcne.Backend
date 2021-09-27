from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.first_name = first_name
        user.last_name = last_name
        user.username = email
        user.save(using=self._db)
        return user


class AuthUser(AbstractUser):
    email = models.EmailField(blank=False, max_length=254, unique=True, verbose_name="email address")
    first_name = models.CharField(blank=False, max_length=254, verbose_name="first name")
    last_name = models.CharField(blank=False, max_length=254, verbose_name="last name")
    dob = models.DateField(blank=True, null=True, verbose_name="date of birth")
    state = models.CharField(blank=False, max_length=254, verbose_name="last name")
    phone_number = models.CharField(blank=False, max_length=20, verbose_name="phone number")

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']
    GET_OBJECT_FIELD = 'name'
