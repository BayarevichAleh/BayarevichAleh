from django import forms
from .models import *
from django.template.base import TemplateSyntaxError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from ckeditor.widgets import CKEditorWidget



class AddMessageForm(forms.ModelForm):
    """
    form for add message
    """

    class Meta:
        model = Message
        fields = ['text']
        widgets = {
            'text': CKEditorWidget(attrs={'class': 'form-control','rows':7,'cols':100}),
        }


class CreateForumForm(forms.ModelForm):
    """
    form for create forum
    """

    class Meta:
        model = Forum
        fields = ['category', 'name', 'commit', 'logo', 'is_pablished']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'commit': CKEditorWidget(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(),
            'is_pablished': forms.CheckboxInput(),
        }


class RegForm(UserCreationForm):
    """
    form for registration user
    """
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
        login = self.cleaned_data['username']
        try:
            login2 = Users.objects.get(login__iexact=login)
            return login2
        except:
            return login


class UserLoginForm(AuthenticationForm):
    """
    form for login user
    """
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title','commit']
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'commit':forms.Textarea(attrs={'class':'form-control'}),
        }

