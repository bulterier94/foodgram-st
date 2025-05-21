from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CustomPasswordValidator:
    def __init__(self):
        self.min_length = 8
        self.require_uppercase = True
        self.require_special_char = True

    def validate(self, password, user=None):
        errors = []

        if len(password) < self.min_length:
            errors.append(
                _(f'Пароль должен содержать минимум {self.min_length} символов')
            )

        if (
            self.require_uppercase
            and not any(char.isupper() for char in password)
        ):
            errors.append(
                _('Пароль должен содержать хотя бы одну заглавную букву')
            )

        if (
            self.require_special_char
            and not any(not char.isalnum() for char in password)
        ):
            errors.append(
                _('Пароль должен содержать хотя бы один специальный символ')
            )

        if errors:
            raise ValidationError(errors)

        return password

    def get_help_text(self):
        rules = [
            _(f'Минимум {self.min_length} символов'),
            _('Хотя бы одна заглавная буква'),
            _('Хотя бы один специальный символ'),
        ]
        return _('Пароль должен содержать: \n') + ',\n'.join(rules) + '.'
