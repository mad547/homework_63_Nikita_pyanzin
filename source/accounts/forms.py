from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from accounts.models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )
    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
    )
    password2 = forms.CharField(
        label='Подвердите пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': 'Подтвердите пароль'}),
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким Email уже существует')
        return cleaned_data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': 'О себе'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон'}),
            'gender': forms.Select(attrs={'class': 'form-control'})
        }


class ProfileEditForm(forms.ModelForm):
    class Meta(UserChangeForm):
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }


class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        label='Логин или Email',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин или Email'}),
    )
    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )