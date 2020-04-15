import csv
from typing import List

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from library.models import Author

FILEPATH_ARG = 'file'
AUTHOR_NAME_CSV_KEY = 'name'


class Command(BaseCommand):
    help = 'Import authors from CSV file and store in the database'

    def add_arguments(self, parser):
        parser.add_argument(FILEPATH_ARG, type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        filepath = options[FILEPATH_ARG]

        self.stdout.write(self.style.SUCCESS('Importing authors...'))

        authors = self.import_authors_from_file_and_save_to_database(filepath)

        total_authors = len(authors)
        success_message = f'1 author imported.' if total_authors == 1 else f'{total_authors} authors imported.'

        self.stdout.write(self.style.SUCCESS(success_message))

    def import_authors_from_file_and_save_to_database(self, filepath: str) -> List[Author]:
        names = self.get_authors_names_from_file(filepath)

        return Author.bulk_create(names)

    def get_authors_names_from_file(self, filepath: str) -> List[str]:
        try:
            with open(filepath) as file:
                csv_reader = csv.DictReader(file)

                return [row[AUTHOR_NAME_CSV_KEY] for row in csv_reader if row[AUTHOR_NAME_CSV_KEY]]
        except FileNotFoundError:
            raise CommandError(f'File not found: "{filepath}"')
        except KeyError:
            raise CommandError(
                f'The "{AUTHOR_NAME_CSV_KEY}" column is missing from the header in the "{filepath}" file'
            )
