import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from library.models import Author, Book


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


class BookModelTest(TestCase):
    fixtures = ['test_data']

    @classmethod
    def setUpTestData(cls):
        cls.books = Book.objects.all()
        cls.author = Author.objects.first()

    def create_test_book(self, name='Test Book', edition=1, publication_year=2020):
        book = Book.objects.create(name=name, edition=edition, publication_year=publication_year)

        book.authors.add(self.author)

        return book

    def test_create_valid_book(self):
        books_count_before = self.books.count()

        self.create_test_book()

        self.assertEqual(self.books.count(), books_count_before + 1)

    def test_create_book_sanitize_name(self):
        name = '  Test Book  \t'
        book = self.create_test_book(name=name)

        self.assertEqual(name.strip(), book.name)

    def test_create_book_with_blank_name(self):
        blank_names = ['', ' ', '\t', '\n', None]

        books_count_before = self.books.count()

        for blank_name in blank_names:
            with self.subTest(book_name=blank_name):
                with self.assertRaises(ValidationError):
                    self.create_test_book(name=blank_name)

        self.assertEqual(self.books.count(), books_count_before)

    def test_create_book_with_invalid_edition(self):
        invalid_editions = [-1, None]

        books_count_before = self.books.count()

        for invalid_edition in invalid_editions:
            with self.subTest(book_edition=invalid_edition):
                with self.assertRaises(ValidationError):
                    self.create_test_book(edition=invalid_edition)

        self.assertEqual(self.books.count(), books_count_before)

    def test_create_book_with_invalid_publication_year(self):
        today = datetime.date.today()
        next_year = today.year + 1

        invalid_years = [-1, next_year, None]

        books_count_before = self.books.count()

        for invalid_year in invalid_years:
            with self.subTest(book_publication_year=invalid_year):
                with self.assertRaises(ValidationError):
                    self.create_test_book(publication_year=invalid_year)

        self.assertEqual(self.books.count(), books_count_before)
