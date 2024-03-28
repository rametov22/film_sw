from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def starts_with_uppercase_validator(value):
    if not value[0].isupper():
        raise ValidationError(
            _('The name should start with an uppercase letter.'),
            params={'value': value},
        )


def contains_only_letters_validator(value):
    if not value.replace(" ", "").isalpha():
        raise ValidationError(
            _('The name should contain only letters.'),
            params={'value': value},
        )


def age_validator(value):
    from datetime import datetime
    current_year = datetime.now().year
    if value.year > current_year:
        raise ValidationError(
            _('Invalid age.'),
            params={'value': value},
        )

