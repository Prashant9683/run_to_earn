from django.contrib.auth.models import AbstractUser
from django.contrib.auth.password_validation import validate_password
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(
        unique=True,
        verbose_name='Email Address'
    )
    first_name = models.CharField(
        max_length=50,
        default='',
        blank=True,
        verbose_name='First Name',
        validators=[
            MaxLengthValidator(50)
        ]
    )
    last_name = models.CharField(
        max_length=50,
        default='',
        blank=True,
        verbose_name='Last Name',
        validators=[
            MaxLengthValidator(50)
        ]
    )

    phone = PhoneNumberField(
        null=True, blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def set_password(self, raw_password):
        validate_password(password=raw_password, user=self)
        return super().set_password(raw_password)

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email