from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'username', 'password1', 'password2', 'main_name', 'nickname', 'email'
        ]


class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = CustomUser
        fields = ['nickname','bio']