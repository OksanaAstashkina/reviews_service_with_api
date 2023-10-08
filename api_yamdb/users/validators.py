"""Валидаторы для приложения Users."""

import re
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError


class CustomUsernameValidator:
    """Валидация введенного username."""

    invalid_chars = '@, ., +, -'

    def __call__(self, value):
        """Проверка введенного username на наличие недопустимых символов.

        Запрет на использование пользовательского имени <me>.
        """
        pattern = r'^[\w.@+-]{1,150}$'
        if re.search(pattern, value) is None:
            invalid_chars_list = [char for char in value if char not in r'\w']
            invalid_chars = ', '.join(invalid_chars_list)
            raise ValidationError(
                f'Недопустимые символы в нике: "{value}". '
                'Допустимы только буквы, цифры и следующие символы: '
                f'{self.invalid_chars}'
                f'Обнаружены следующие недопустимые символы: {invalid_chars}.'
            )
        if value.lower() == 'me':
            raise ValidationError('Имя пользователя не может быть "me".')


class CustomEmailValidator(EmailValidator):
    """Валидация введенного e-mail."""

    invalid_chars = '@, ., +, -'

    def __call__(self, value):
        """Проверка введенного e-mail на наличие недопустимых символов."""
        super().__call__(value)
        pattern = r'^[\w.@+-]{1,254}$'
        if re.search(pattern, value) is None:
            invalid_chars_list = [char for char in value if char not in r'\w']
            invalid_chars = ', '.join(invalid_chars_list)
            raise ValidationError(
                f'Недопустимые символы в адресе электронной почты: {value}. '
                'Допустимы только буквы, цифры и следующие символы: '
                f'{self.invalid_chars}.'
                f'Обнаружены следующие недопустимые символы: {invalid_chars}.'
            )


def validate_username(value):
    """Вызов валдатора username."""
    CustomUsernameValidator()(value)


def validate_email(value):
    """Вызов валдатора e-mail."""
    CustomEmailValidator(EmailValidator)(value)
