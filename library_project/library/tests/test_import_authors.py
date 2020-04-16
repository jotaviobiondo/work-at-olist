from io import StringIO
import os
import csv
import tempfile
from typing import List

from django.core.management import call_command, CommandError
from django.test import TestCase

from library.models import Author


class ImportAuthorsTest(TestCase):

    def setUp(self):
        self.csvfile = tempfile.NamedTemporaryFile(mode='w', delete=False, newline='')
        self.filename = self.csvfile.name

        self.authors = Author.objects.all()

    def tearDown(self):
        os.unlink(self.filename)

    def write_content_to_file(self, content: List[str], header_column='name'):
        self.writer = csv.DictWriter(self.csvfile, fieldnames=[header_column])

        self.writer.writeheader()

        for item in content:
            self.writer.writerow({header_column: item})

        self.csvfile.close()

    def call_import_authors_command(self):
        command_args = [self.filename]

        call_command('import_authors', *command_args, stdout=StringIO())

    def authors_as_names_list(self):
        return [author.name for author in self.authors]

    def test_empty_file(self):
        self.write_content_to_file([])
        self.call_import_authors_command()

        self.assertEqual(self.authors.count(), 0)

    def test_file_with_valid_content(self):
        author_names = ['William Shakespeare', 'William Faulkner', 'Jane Austen']

        self.write_content_to_file(author_names)
        self.call_import_authors_command()

        self.assertEqual(self.authors.count(), len(author_names))
        self.assertListEqual(self.authors_as_names_list(), author_names)

    def test_file_with_blank_lines_content(self):
        author_names = ['William Shakespeare', '', 'Jane Austen', '']

        self.write_content_to_file(author_names)
        self.call_import_authors_command()

        authors_names_not_blank = [name for name in author_names if name]

        self.assertEqual(self.authors.count(), len(authors_names_not_blank))
        self.assertListEqual(self.authors_as_names_list(), authors_names_not_blank)

    def test_invalid_header_column_name(self):
        author_names = ['William Shakespeare', 'William Faulkner', 'Jane Austen']

        self.write_content_to_file(author_names, header_column='wrong')

        with self.assertRaises(CommandError):
            self.call_import_authors_command()

        self.assertEqual(self.authors.count(), 0)

    def test_reimport_same_file(self):
        author_names = ['William Shakespeare', 'William Faulkner', 'Jane Austen']

        self.write_content_to_file(author_names)

        self.call_import_authors_command()

        self.assertEqual(self.authors.count(), len(author_names))

        with self.assertRaises(CommandError):
            self.call_import_authors_command()

        self.assertEqual(self.authors.count(), len(author_names))
