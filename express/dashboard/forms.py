from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

class WalletCreationForm(forms.Form):
    coin_choices = (
        ('btc', 'Bitcoin'),
        ('eth', 'Ethereum'),
        # Add more coins if necessary
    )
    coin = forms.ChoiceField(choices=coin_choices)
    label = forms.CharField(max_length=100, required=False)