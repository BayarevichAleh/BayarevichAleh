from django import forms
from .models import *
from django.template.base import TemplateSyntaxError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.core.exceptions import ValidationError



class RegForm(UserCreationForm):
    password1 = forms.CharField(label='Пароль', max_length=100,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повтор пароля', max_length=100,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Users
        fields = ['username', 'email', 'first_name', 'last_name', 'age', 'photo']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            # 'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.DateInput(attrs={'class': 'form-control', 'data-target': '#datetimepicker1'}),
            'photo': forms.FileInput()
        }

    def clean_login(self):
        photo = self.cleaned_data['photo']
        print(photo)
        login = self.cleaned_data['username']
        try:
            login2 = Users.objects.get(login__iexact=login)
            return login2
        except:
            return login


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

