import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_is_not_blank(value: str):
    if value is None or value.strip() == '':
        raise ValidationError(_('This field cannot be blank.'), params={'value': value})


def validate_earlier_than_current_year(value: int):
    today = datetime.date.today()
    if value > today.year:
        raise ValidationError(_('%(value)s must be earlier or equal to current year.'), params={'value': value})
