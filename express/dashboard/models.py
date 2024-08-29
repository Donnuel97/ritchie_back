from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.core.mail import send_mail


class UserForm(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, validators=[MinLengthValidator(8)])
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    phone_number = models.CharField(max_length=11, null=True)

    def save(self, *args, **kwargs):
        # Hash the password before saving to the database
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
