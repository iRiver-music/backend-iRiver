import datetime
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxLengthValidator
from django.contrib.auth.forms import UserCreationForm

#國家清單
country=(
    ('NN','不透露'),
    ('US','United States'),
    ('CA','Canada'),
    ('JP','Japan'),
    ('CN','China'),
    ('TW','Taiwan'),
    ('KR','Korea'),
    ('SG','Singapore'),
    ('MY','Malaysia'),
    ('TH','Thailand'),
    ('PH','Philippines'),
    ('ID','Indonesia'),
)

#性別清單
gender=(
    ('U','不透露'),
    ('M','男'),
    ('F','女'),
)

class login(models.Model):
    pass






class RegisterForm(UserCreationForm):
    username=forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email=forms.EmailField(
        label="電子郵件",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1=forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2=forms.CharField(
        label="密碼確認",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model=User
        fields=('username','email','password1','password2')

class LoginForm(forms.Form):
    username=forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password=forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

