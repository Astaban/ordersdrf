from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm


class UserRegisterForm(UserCreationForm):
    username = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]
        labels = {
            'username': 'Имя пользователя:',
            'first_name': 'Имя:',
            'last_name': 'Фамилия:',
            'email': 'Почта:',
            'password1': 'Введите пароль:',
            'password2': 'Подтвердите пароль:',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'user_login', }),
            'first_name': forms.TextInput(attrs={'class': 'user_login', }),
            'last_name': forms.TextInput(attrs={'class': 'user_login', }),
            'email': forms.EmailInput(attrs={'class': 'user_login', }),
            'password1': forms.PasswordInput(attrs={'class': 'user_login', }),
            'password2': forms.PasswordInput(attrs={'class': 'user_login', }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Такой адрес уже зарегистрирован')
        return email


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(
            attrs={'class': 'user_login', }
        )
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={'class': 'user_login', }
        )
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(
        disabled=True,
        label='Имя пользователя:',
        widget=forms.TextInput(attrs={'class': 'user_login', })
    )
    email = forms.CharField(
        disabled=True,
        label='Почта:',
        widget=forms.EmailInput(attrs={'class': 'user_login', })
    )

    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]
        labels = {
            'first_name': 'Имя:',
            'last_name': 'Фамилия:',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'user_login', }),
            'last_name': forms.TextInput(attrs={'class': 'user_login', }),
        }


class UserPasswordChangeForm(PasswordChangeForm):

    old_password = forms.CharField(
        label="Старый пароль:",
        widget=forms.PasswordInput(attrs={'class': 'user_login', }),
    )
    new_password1 = forms.CharField(
        label="Введите новый пароль:",
        widget=forms.PasswordInput(attrs={'class': 'user_login', }),
    )
    new_password2 = forms.CharField(
        label="Подтвердите новый пароль:",
        widget=forms.PasswordInput(attrs={'class': 'user_login', }),
    )
