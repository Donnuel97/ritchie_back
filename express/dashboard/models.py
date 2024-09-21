from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.core.mail import send_mail
from django.utils import timezone

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

class Wallet(models.Model):
    user = models.ForeignKey(UserForm, on_delete=models.CASCADE, related_name='wallet')
    wallet_address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username}'s Wallet"


class Transaction(models.Model):
    STATUS_CHOICES = (
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    )

    user = models.ForeignKey('UserForm', on_delete=models.CASCADE)
    transaction_hash = models.CharField(max_length=255, blank=True, null=True)
    recipient_address = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=20, decimal_places=10)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='FAILED')
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Transaction {self.transaction_hash or 'Unsuccessful'} for {self.user.username}"