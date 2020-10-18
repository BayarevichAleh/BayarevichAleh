from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import *


class AddMessageForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget(attrs={'class': 'form-control', 'rows': 7, 'cols': 100}))
    class Meta:
        model = Message
        fields = ['text']


class CreateForumForm(forms.ModelForm):
    commit = forms.CharField(widget=CKEditorWidget(attrs={'class': 'form-control', 'rows': 7, 'cols': 100}))
    class Meta:
        model = Forum
        fields = ['category', 'name', 'commit', 'logo', 'is_published']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'commit': CKEditorWidget(attrs={'class': 'form-control', 'rows': 7, 'cols': 100}),
            'logo': forms.FileInput(),
            'is_published': forms.CheckboxInput(),
        }


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Пароль', max_length=100,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повтор пароля', max_length=100,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Users
        fields = ['username', 'email', 'first_name', 'last_name', 'age', 'photo']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.DateInput(attrs={'class': 'form-control', 'data-target': '#datetimepicker1'}),
            'photo': forms.FileInput()
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if Users.objects.filter(username__iexact=username).exists():
            return Users.objects.get(username__iexact=username)
        return username


class EditUserForm(UserChangeForm):
    class Meta:
        model = Users
        fields = ['email', 'first_name', 'last_name', 'age', 'photo']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.DateInput(attrs={'class': 'form-control', 'data-target': '#datetimepicker1'}),
            'photo': forms.FileInput()
        }


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if Users.objects.filter(username__iexact=username).exists():
            return Users.objects.get(username__iexact=username)
        return username


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'commit']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'commit': forms.Textarea(attrs={'class': 'form-control'}),
        }
