import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from library.validators import validate_is_not_blank, validate_earlier_than_current_year


class ValidateIsNotBlankTestCase(TestCase):
    def test_blank_values(self):
        blank_values = ['', ' ', '  ', '\t', '\n', None]

        for value in blank_values:
            with self.subTest(value=value):
                with self.assertRaises(ValidationError):
                    validate_is_not_blank(value)

    def test_not_blank_value(self):
        try:
            validate_is_not_blank('Not blank')
        except ValidationError:
            self.fail('A non-blank value must not raise exception.')


class ValidateEarlierThanCurrentYearTestCase(TestCase):
    def setUp(self):
        today = datetime.date.today()
        self.current_year = today.year

    def test_future_year(self):
        with self.assertRaises(ValidationError):
            validate_earlier_than_current_year(self.current_year + 1)

    def test_current_year(self):
        try:
            validate_earlier_than_current_year(self.current_year)
        except ValidationError:
            self.fail('Current year must not raise exception.')

    def test_past_year(self):
        try:
            validate_earlier_than_current_year(self.current_year - 1)
        except ValidationError:
            self.fail('Past years must not raise exception.')
