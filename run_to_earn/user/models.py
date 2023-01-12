from django.contrib.auth.models import AbstractUser
from django.contrib.auth.password_validation import validate_password
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(models.Model):
    id = models.AutoField(primary_key=True)

    first_name = models.CharField(
        max_length=50,
        default='',
        blank=False,
        null=False,
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

    email = models.EmailField(
        unique=True,
        verbose_name='Email Address'
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

class RefreshTokens(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    refreshToken = models.CharField(max_length=255)
    issued = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "refreshTokens"
        verbose_name_plural = "Refresh Tokens"
        verbose_name = "Refresh Token"

    def __str__(self):
        return self.refreshToken

__all__ = [
    'RefreshTokens'
]


class VerificationOTP(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        verbose_name='User'
    )
    otp = models.CharField(
        max_length=50,
        verbose_name='OTP'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.otp}'

    class Meta:
        verbose_name = 'Verification OTP'
        verbose_name_plural = 'Verification OTPs'

class Goal(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        verbose_name='User'
    )
    goal = models.PositiveIntegerField(
        verbose_name='Goal'
    )

    class Meta:
        db_table = 'goal'
        verbose_name = 'Goal'
        verbose_name_plural = 'Goals'

    def __str__(self):
        return self.goal