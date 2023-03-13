from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from datetime import date
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """User model used for authentication and microblog authoring."""

    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^\w{3,}$',
            message='Username must consist of @ followed by at least three alphanumericals'
        )]
    )
    email = models.EmailField(unique=True, blank=False)
    credit_card = models.CharField(max_length=16, blank=True, null=True, validators=[RegexValidator(r'^\d{16}$', 'Must be 16 digits.')])
    dob = models.DateField()

class Payment(models.Model):
    credit_card = models.CharField(max_length=16, blank=True, null=True, validators=[RegexValidator(r'^\d{16}$', 'Must be 16 digits.')])
    amount = models.CharField(max_length=3, blank=False, null=False, validators=[RegexValidator(r'^\d{3}$', 'Must be 3 digits.')])