from django import forms
from django.core.validators import RegexValidator
from .models import User, Payment

class LogInForm(forms.Form):

    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())



class RegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email','dob' ,'credit_card']

        password = forms.CharField(label = 'Password', widget = forms.PasswordInput())
        password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment

        fields = ['credit_card', 'amount']
