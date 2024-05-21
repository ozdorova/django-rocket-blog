import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       UserCreationForm)


class LoginUserForm(AuthenticationForm):
    # форма для входа в систему
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': "form-control mr-0 ml-auto"}),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={'class': "form-control mr-0 ml-auto"}),
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    # форма регистрации
    # проверки пароля уже есть в UserCreationForm
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': "form-control mr-0 ml-auto"}),
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={'class': "form-control mr-0 ml-auto"}),
    )
    password2 = forms.CharField(
        label='Повтор пароля',
        widget=forms.PasswordInput(
            attrs={'class': "form-control mr-0 ml-auto"}),
    )

    class Meta:
        # получение модели бд пользователя
        model = get_user_model()
        # отображаемые поля
        fields = [
            'username', 'email', 'first_name', 'last_name', 'password1', 'password2',
        ]
        # дополнительные наименования полей
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        # стили оформления полей
        widgets = {
            'email': forms.TextInput(attrs={'class': "form-control mr-0 ml-auto"}),
            'first_name': forms.TextInput(attrs={'class': "form-control mr-0 ml-auto"}),
            'last_name': forms.TextInput(attrs={'class': "form-control mr-0 ml-auto"}),
        }

    def clean(self):
        # проверка почты на уникальность
        cleaned_data = super().clean()
        User = get_user_model()
        if User.objects.filter(email=cleaned_data.get('email')).exists():
            raise forms.ValidationError("Эта почта уже зарегестрированна")
        return cleaned_data


class ProfileUserForm(forms.ModelForm):
    # форма для отображение профиля profile.html
    username = forms.CharField(
        disabled=True,
        label='Логин',
        widget=forms.TextInput(attrs={'class': "form-control mr-0 ml-auto"}),
    )
    email = forms.CharField(
        required=False,
        disabled=True,
        label='E-mail',
        widget=forms.TextInput(attrs={'class': "form-control mr-0 ml-auto"}),
    )
    this_year = datetime.date.today().year
    date_birth = forms.DateField(
        widget=forms.SelectDateWidget(
            years=tuple(range(this_year-100, this_year-5))
        ),
    )

    class Meta:
        model = get_user_model()
        fields = [
            'photo', 'username', 'email', 'date_birth', 'first_name', 'last_name',
        ]
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': "form-control mr-0 ml-auto"}),
            'last_name': forms.TextInput(attrs={'class': "form-control mr-0 ml-auto"}),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Старый пароль',
        widget=forms.PasswordInput(
            attrs={'class': "form-control mr-0 ml-auto"}),
    )
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(
            attrs={'class': "form-control mr-0 ml-auto"}),
    )
    new_password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(
            attrs={'class': "form-control mr-0 ml-auto"}),
    )

