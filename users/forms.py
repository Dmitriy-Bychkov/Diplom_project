from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import User
from django import forms


class StyleFormMixin:
    """ Класс-миксин для стилизации форм """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != "is_active":
                field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """ Форма регистрации нового пользователя """

    class Meta:
        """ Отображение нужных нам полей в форме регистрации пользователя """

        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone",
            "country",
            "avatar",
            "password1",
            "password2"
        ]


class UserProfileForm(StyleFormMixin, UserChangeForm):
    """ Форма профиля пользователя """

    class Meta:
        """ Отображение нужных нам полей в форме профиля пользователя """

        model = User
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "phone",
            "country",
            "avatar"
        ]

    def __init__(self, *args, **kwargs):
        """ Скрытие поля с паролем """

        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class PasswordForm(StyleFormMixin, forms.Form):
    """ Форма смены пароля пользователем """

    new_password = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput
    )
    confirm_password = forms.CharField(
        label='Подтвердите пароль',
        widget=forms.PasswordInput
    )

    def clean(self):
        """
        Используется в форме для выполнения дополнительной валидации данных,
        переданных пользователем и чтобы получить очищенные данные формы.
        Метод проверяет, что значения полей new_password
        и confirm_password совпадают
        """

        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if (new_password and confirm_password
                and new_password != confirm_password):
            raise forms.ValidationError('Пароли не совпадают')

        return cleaned_data
