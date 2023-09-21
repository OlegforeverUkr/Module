from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from booksapp.models import Author, Genre
from django.contrib.auth.models import User

UserModel = get_user_model()


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={
            'class': "form-control form-control-xs", 
            'name': 'username',
            'placeholser': 'Username'
        }
    ))

    first_name = forms.CharField(label='First Name', widget=forms.TextInput(
        attrs={
            'class': "form-control form-control-xs", 
            'name': 'first_name',
            'placeholser': 'First Name'
        }
    ))

    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(
        attrs={
            'class': "form-control form-control-xs", 
            'name': 'last_name',
            'placeholser': 'Last Name'
        }
    ))

    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': "form-control form-control-xs", 
            'name': 'password',
            'placeholser': 'Password'
             }))

    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={
            'class': "form-control form-control-xs", 
            'name': 'confirm_password',
            'placeholser': 'Confirm Password'
             }))

    def create_user(self):
        del self.cleaned_data['confirm_password']
        UserModel.objects.create_user(**self.cleaned_data)


    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            if UserModel.objects.get(username=username):
                raise ValidationError('User with the same username already exists')
        except UserModel.DoesNotExist:
            return username


    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            self.add_error('password', 'Does not match')
            self.add_error('confirm_password', 'Does not match')


    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name:
            raise ValidationError('First name is required')
        return first_name


    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name:
            raise ValidationError('Last name is required')
        return last_name

class CreateAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name_author', 'bio_author']
        widgets = {
            'name_author': forms.TextInput(attrs={'class': "form-control form-control-xs", 'placeholder': 'Name author'}),
            'bio_author': forms.Textarea(attrs={'class': "form-control form-control-xs", 'placeholder': 'Author Biography'}),
        }

class CreateGenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name_genre']
        widgets = {
            'name_genre': forms.TextInput(attrs={'class': "form-control form-control-xs", 'placeholder': 'Genre name'}),
        }
