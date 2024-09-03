from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'role',
                  'bio',)


class CustomUserChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'role',
                  'bio',)
