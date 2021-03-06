from __future__ import annotations

import uuid
from typing import List

from django.core.validators import MinValueValidator
from django.db import models, transaction

from library.validators import validate_is_not_blank, validate_earlier_than_current_year


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
            self.name = strip_and_remove_duplicate_spaces(self.name)

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
    authors = models.ManyToManyField(Author, related_name='books')

    class Meta:
        verbose_name = 'book'
        verbose_name_plural = 'books'

    def __str__(self):
        return self.name

    def clean(self):
        if self.name:
            self.name = strip_and_remove_duplicate_spaces(self.name)


def strip_and_remove_duplicate_spaces(value: str) -> str:
    """
    Return a copy of the string removing all leading, trailing and duplicate whitespace in the middle.
    """
    return ' '.join(value.split())
