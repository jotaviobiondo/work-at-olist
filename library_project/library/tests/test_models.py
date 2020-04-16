from django.core.exceptions import ValidationError
from django.test import TestCase

from library.models import Author


class AuthorModelTest(TestCase):
    author_names = [
        'Luciano Ramalho',
        'Osvaldo Santana Neto',
        'David Beazley',
        'Chetan Giridhar',
        'Brian K. Jones',
        'J.K Rowling'
    ]

    existing_author_name = author_names[0]

    @classmethod
    def setUpTestData(cls):
        for name in cls.author_names:
            Author.objects.create(name=name)

        cls.authors_count_before = Author.objects.all().count()

    def test_create_valid_author(self):
        Author.objects.create(name='George R. R. Martin')

        authors_count_now = Author.objects.all().count()

        self.assertEqual(authors_count_now, self.authors_count_before + 1)

    def test_create_existing_author(self):
        with self.assertRaises(ValidationError):
            Author.objects.create(name=self.existing_author_name)

        authors_count_now = Author.objects.all().count()
        self.assertEqual(authors_count_now, self.authors_count_before)

    def test_create_author_with_blank_name(self):
        blank_names = ['', ' ', '\t', '\n', None]

        for blank_name in blank_names:
            with self.subTest(author_name=blank_name):
                with self.assertRaises(ValidationError):
                    Author.objects.create(name=blank_name)

        authors_count_now = Author.objects.all().count()
        self.assertEqual(authors_count_now, self.authors_count_before)

    def test_create_author_sanitize_name(self):
        name = '  George R. R. Martin  \t'
        author = Author.objects.create(name=name)

        authors_count_now = Author.objects.all().count()
        self.assertEqual(authors_count_now, self.authors_count_before + 1)
        self.assertEqual(name.strip(), author.name)

    def test_bulk_create_valid_authors(self):
        new_authors_names = ['William Shakespeare', 'William Faulkner', 'Henry James', 'Jane Austen']
        new_authors = Author.bulk_create(new_authors_names)

        authors_count_now = Author.objects.all().count()

        self.assertEqual(authors_count_now, self.authors_count_before + len(new_authors))

    def test_bulk_create_invalid_authors(self):
        invalid_authors_names = [self.existing_author_name, '', ' ', '\t', None]

        for author_name in invalid_authors_names:
            with self.subTest(author_name=author_name):
                with self.assertRaises(ValidationError):
                    Author.bulk_create([author_name])

        authors_count_now = Author.objects.all().count()
        self.assertEqual(authors_count_now, self.authors_count_before)
