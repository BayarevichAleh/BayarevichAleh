from django import forms
from .models import *
from django.template.base import TemplateSyntaxError


class RegForm(forms.ModelForm):
    password2 = forms.CharField(label='Повтор пароля', max_length=100,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['login', 'password', 'email', 'name', 'lastname', 'age', 'photo']
        widgets = {
            'login': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.DateInput(attrs={'class': 'form-control', 'data-target': '#datetimepicker1'}),
            'photo': forms.FileInput
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']

    def clean_login(self):
        login = self.cleaned_data['login']
        try:
            login2 = User.objects.get(login__iexact=login)
            return login2
        except:
            return login
