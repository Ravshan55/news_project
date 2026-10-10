from django import forms
from django.contrib.auth.forms import UsernameField
from django.forms.widgets import PasswordInput
from django.contrib.auth.models import User
from .models import Profile

class LoginFrom(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password_2 = forms.CharField(label="Type password again", widget=PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password_2']:
            raise forms.ValidationError("Both passwords should match!")
        return data['password_2']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']