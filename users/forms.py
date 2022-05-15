from cProfile import label
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'fathers_name','email', 'role')
        labels = {
            'last_name': 'Фамилия',
            'first_name': 'Имя',
            'fathers_name': 'Отчество',
            'email': 'Адрес электронной почты',
            'role': 'Права доступа',
        }


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)

