from __future__ import annotations

import uuid
from typing import List

from django.db import models, transaction


class AbstractBaseModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Author(AbstractBaseModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'author'
        verbose_name_plural = 'authors'

    def __str__(self):
        return self.name

    @staticmethod
    @transaction.atomic
    def bulk_create(author_names: List[str]) -> List[Author]:
        authors = [Author(name=author_name) for author_name in author_names]

        return Author.objects.bulk_create(authors)
