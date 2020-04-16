from __future__ import annotations

import datetime
import uuid
from typing import List

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _


def validate_is_not_blank(value: str):
    if value is None or value.strip() == '':
        raise ValidationError(_('This field cannot be blank.'), params={'value': value})


def validate_earlier_than_current_year(value: int):
    today = datetime.date.today()
    if value > today.year:
        raise ValidationError(_('%(value)s must be earlier or equal to current year.'), params={'value': value})


class AbstractBaseModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Author(AbstractBaseModel):
    name = models.CharField(max_length=100, unique=True, validators=[validate_is_not_blank])

    class Meta:
        verbose_name = 'author'
        verbose_name_plural = 'authors'

    def __str__(self):
        return self.name

    def clean(self):
        if self.name:
            self.name = self.name.strip()

    def unique_error_message(self, model_class, unique_check):
        return f'Author with the name "{self.name}" already exists.'

    @staticmethod
    @transaction.atomic
    def bulk_create(author_names: List[str]) -> List[Author]:
        authors = [Author(name=author_name) for author_name in author_names]

        for author in authors:
            author.full_clean()

        return Author.objects.bulk_create(authors)


class Book(AbstractBaseModel):
    name = models.CharField(max_length=50, validators=[validate_is_not_blank])
    edition = models.PositiveSmallIntegerField(validators=[MinValueValidator(limit_value=1)])
    publication_year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(limit_value=1), validate_earlier_than_current_year]
    )
    authors = models.ManyToManyField(Author)

    class Meta:
        verbose_name = 'book'
        verbose_name_plural = 'books'

    def __str__(self):
        return self.name

    def clean(self):
        if self.name:
            self.name = self.name.strip()
