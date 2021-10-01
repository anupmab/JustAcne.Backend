from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, password=None, is_admin=False, is_staff=False,
                    is_active=True, is_superuser=False, **extra_fields):
        if not email:
            raise ValueError("User must have an email")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)  # change password to hash
        user.is_admin = is_admin
        user.is_staff = is_staff
        user.is_active = is_active
        user.username = email
        user.is_superuser = is_superuser
        user.access_type = 'ADMIN'
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name='', last_name='', password=None, **extra_fields):
        user = self.create_user(email, first_name, last_name, password, True, True, True, True, **extra_fields)
        return user


class AuthUser(AbstractUser):
    email = models.EmailField(blank=False, max_length=254, unique=True, verbose_name="email address")
    first_name = models.CharField(blank=True, max_length=254, verbose_name="first name")
    last_name = models.CharField(blank=True, max_length=254, verbose_name="last name")
    dob = models.DateField(blank=True, null=True, verbose_name="date of birth")
    state = models.CharField(blank=True, max_length=254, verbose_name="state")
    phone_number = models.CharField(blank=True, max_length=20, verbose_name="phone number")
    billing_address = models.JSONField(default=dict)
    shipping_address = models.JSONField(default=dict)
    checkout_info = models.JSONField(default=dict)
    access_type = models.CharField(max_length=20, default='USER', choices=(('USER', 'USER'), ('ADMIN', 'ADMIN')))

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []
    GET_OBJECT_FIELD = 'name'


def get_image_upload_path(instance, filename):
    return "user_images/{}/{}".format(instance.id, filename)


class UserImage(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to=get_image_upload_path)
