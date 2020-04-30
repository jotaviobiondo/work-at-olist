import uuid
from typing import List

from rest_framework import status
from rest_framework.test import APITestCase

from library.models import Author, Book


class BaseRestApiTest(APITestCase):
    base_url = None

    def list(self, query=None):
        if query is None:
            query = {}

        return self.client.get(self.base_url, query, format='json')

    def retrieve(self, resource_id):
        return self.client.get(self.base_url + f'{resource_id}/', format='json')

    def create(self, payload):
        return self.client.post(self.base_url, payload, format='json')

    def update(self, resource_id, payload):
        return self.client.put(self.base_url + f'{resource_id}/', payload, format='json')

    def delete(self, resource_id):
        return self.client.delete(self.base_url + f'{resource_id}/', format='json')

    def assertPaginatedListQueryParams(self, page_query_param, page_size_query_param):
        """
        Asserts that the list endpoint is paginated and accepts 'page_query_param' as query parameter to control
        which page is on and 'page_size_query_param' to control the maximum number of results on the page.
        """
        query = {page_query_param: 2, page_size_query_param: 1}
        response = self.list(query)

        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual(response.data.keys(), ['count', 'results', 'next', 'previous'])
        self.assertEqual(len(data['results']), 1)
        self.assertIsNotNone(data['next'])
        self.assertIsNotNone(data['previous'])

    def assert404NotFound(self, response):
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertCountEqual(response.data.keys(), ['detail'])
        self.assertIsInstance(response.data['detail'], str)

    def assertSearchHasNoResults(self, response):
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertListEqual(response.data['results'], [])

    def assert400BadRequestWithErrors(self, response, fields_with_errors):
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertCountEqual(response.data.keys(), fields_with_errors)

        for field in fields_with_errors:
            self.assertIsInstance(response.data[field], list)

            for error in response.data[field]:
                self.assertIsInstance(error, str)


class AuthorsApiTest(BaseRestApiTest):
    fixtures = ['test_data']

    base_url = '/api/authors/'

    @classmethod
    def setUpTestData(cls):
        cls.authors = Author.objects.all()

    def author_to_json(self, author: Author):
        return {
            'id': str(author.id),
            'name': author.name
        }

    def test_list(self):
        response = self.list()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], self.authors.count())
        self.assertGreater(len(response.data['results']), 0)

    def test_list_page_query_params(self):
        self.assertPaginatedListQueryParams('page', 'page_size')

    def test_retrieve(self):
        author = self.authors.first()

        response = self.retrieve(author.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, self.author_to_json(author))

    def test_retrieve_nonexistent(self):
        random_uuid = uuid.uuid4()
        response = self.retrieve(random_uuid)

        self.assert404NotFound(response)

    def test_search_name(self):
        author = self.authors.first()

        query = {'name': author.name[:3]}
        response = self.list(query)

        results = response.data['results']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(results), 1)

        for result in results:
            self.assertIn(query['name'].lower(), result['name'].lower())

    def test_search_nonexistent_name(self):
        query = {'name': 'Nonexistent Author'}
        response = self.list(query)

        self.assertSearchHasNoResults(response)

    def test_create_not_allowed(self):
        new_author = {'name': 'New Author'}

        response = self.create(new_author)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_not_allowed(self):
        author = self.authors.first()
        updated_author_payload = {'name': 'Updated Author'}

        response = self.update(author.id, updated_author_payload)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_not_allowed(self):
        author = self.authors.first()

        response = self.delete(author.id)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class BooksApiTest(BaseRestApiTest):
    fixtures = ['test_data']

    base_url = '/api/books/'

    @classmethod
    def setUpTestData(cls):
        cls.books = Book.objects.all()
        cls.authors = Author.objects.all()

    def authors_to_json(self, authors: List[Author]):
        return [
            {
                'id': str(author.id),
                'name': author.name
            }
            for author in authors
        ]

    def book_to_json(self, book: Book):
        return {
            'id': str(book.id),
            'name': book.name,
            'edition': book.edition,
            'publication_year': book.publication_year,
            'authors': self.authors_to_json(book.authors.all())
        }

    def test_list(self):
        response = self.list()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], self.books.count())
        self.assertGreater(len(response.data['results']), 0)

    def test_list_page_query_params(self):
        self.assertPaginatedListQueryParams('page', 'page_size')

    def test_retrieve(self):
        book = self.books.first()

        response = self.retrieve(book.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, self.book_to_json(book))

    def test_retrieve_nonexistent(self):
        random_uuid = uuid.uuid4()
        response = self.retrieve(random_uuid)

        self.assert404NotFound(response)

    def test_search_name(self):
        book = self.books.first()

        query = {'name': book.name[:3]}
        response = self.list(query)

        results = response.data['results']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(results), 1)

        for result in results:
            self.assertIn(query['name'].lower(), result['name'].lower())

    def test_search_nonexistent_name(self):
        query = {'name': 'Nonexistent Book'}
        response = self.list(query)

        self.assertSearchHasNoResults(response)

    def test_search_edition(self):
        query = {'edition': 1}
        response = self.list(query)

        results = response.data['results']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(results), 1)

        for result in results:
            self.assertEqual(result['edition'], query['edition'])

    def test_search_nonexistent_edition(self):
        query = {'edition': 1000}
        response = self.list(query)

        self.assertSearchHasNoResults(response)

    def test_search_publication_year(self):
        book = self.books.first()

        query = {'publication_year': book.publication_year}
        response = self.list(query)

        results = response.data['results']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(results), 1)

        for result in results:
            self.assertEqual(result['publication_year'], query['publication_year'])

    def test_search_nonexistent_publication_year(self):
        query = {'publication_year': 1500}
        response = self.list(query)

        self.assertSearchHasNoResults(response)

    def test_search_author_name(self):
        book = self.books.first()
        author_search_name = book.authors.first().name

        query = {'author': author_search_name}
        response = self.list(query)

        results = response.data['results']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(results), 1)

        for result in results:
            authors = result['authors']

            has_at_least_one_author_with_search_name = any(
                author
                for author in authors
                if author_search_name.lower() in author['name'].lower()
            )

            self.assertTrue(has_at_least_one_author_with_search_name)

    def test_search_nonexistent_author_name(self):
        query = {'author': 'Nonexistent Author'}
        response = self.list(query)

        self.assertSearchHasNoResults(response)

    def test_search_by_multiple_fields(self):
        book = self.books.first()

        query = {
            'name': book.name,
            'edition': book.edition,
            'publication_year': book.publication_year,
            'author': book.authors.first().name
        }
        response = self.list(query)

        results = response.data['results']
        result = results[0]
        author_names = [author['name'] for author in result['authors']]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 1)
        self.assertEqual(result['name'], query['name'])
        self.assertEqual(result['edition'], query['edition'])
        self.assertEqual(result['publication_year'], query['publication_year'])
        self.assertIn(query['author'], author_names)

    def test_search_nonexistent_by_multiple_fields(self):
        book = self.books.first()

        wrong_edition = book.edition + 100
        query = {
            'name': book.name,
            'edition': wrong_edition,
            'publication_year': book.publication_year,
            'author': book.authors.first().name
        }

        response = self.list(query)

        self.assertSearchHasNoResults(response)

    def test_create(self):
        author = self.authors.first()

        new_book = {
            'name': 'New Book',
            'edition': 1,
            'publication_year': 2020,
            'authors': [str(author.id)]
        }

        books_count_before = self.books.count()

        response = self.create(new_book)
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.books.count(), books_count_before + 1)
        self.assertEqual(data['name'], new_book['name'])
        self.assertEqual(data['edition'], new_book['edition'])
        self.assertEqual(data['publication_year'], new_book['publication_year'])
        self.assertEqual(len(data['authors']), 1)
        self.assertEqual(data['authors'][0]['id'], new_book['authors'][0])

        saved_book = self.books.get(pk=data['id'])
        self.assertDictEqual(data, self.book_to_json(saved_book))

    def test_create_invalid(self):
        invalid_books = [
            {},
            {'name': None, 'edition': None, 'publication_year': None, 'authors': None},
            {'name': '', 'edition': -1, 'publication_year': -1, 'authors': []}
        ]

        fields_with_errors = ['name', 'edition', 'publication_year', 'authors']

        books_count_before = self.books.count()

        for invalid_book in invalid_books:
            with self.subTest(invalid_author=invalid_book):
                response = self.create(invalid_book)

                self.assert400BadRequestWithErrors(response, fields_with_errors)

        self.assertEqual(self.books.count(), books_count_before)

    def test_update(self):
        book_to_update = self.books.first()
        book_authors = book_to_update.authors.all()

        different_author = next(author for author in self.authors if author not in book_authors)

        updated_book_authors_payload = [str(author.id) for author in book_authors]
        updated_book_authors_payload.append(str(different_author.id))

        updated_book_payload = {
            'name': 'Updated Book',
            'edition': 2,
            'publication_year': 2000,
            'authors': updated_book_authors_payload
        }

        books_count_before = self.books.count()

        response = self.update(book_to_update.id, updated_book_payload)
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.books.count(), books_count_before)
        self.assertEqual(data['name'], updated_book_payload['name'])
        self.assertEqual(data['edition'], updated_book_payload['edition'])
        self.assertEqual(data['publication_year'], updated_book_payload['publication_year'])
        self.assertEqual(len(data['authors']), len(updated_book_payload['authors']))

        data_authors_ids = [author['id'] for author in data['authors']]
        self.assertSetEqual(set(data_authors_ids), set(updated_book_payload['authors']))

        updated_book = self.books.get(pk=data['id'])
        self.assertDictEqual(data, self.book_to_json(updated_book))

    def test_update_invalid(self):
        book_to_update = self.books.first()

        invalid_updated_book_payloads = [
            {},
            {'name': None, 'edition': None, 'publication_year': None, 'authors': None},
            {'name': '', 'edition': -1, 'publication_year': -1, 'authors': []}
        ]

        fields_with_errors = ['name', 'edition', 'publication_year', 'authors']

        books_count_before = self.books.count()

        for invalid_book in invalid_updated_book_payloads:
            with self.subTest(invalid_author=invalid_book):
                response = self.update(book_to_update.id, invalid_book)
                not_updated_book = self.books.get(pk=book_to_update.id)

                self.assert400BadRequestWithErrors(response, fields_with_errors)
                self.assertEqual(book_to_update.id, not_updated_book.id)
                self.assertEqual(book_to_update.name, not_updated_book.name)
                self.assertEqual(book_to_update.edition, not_updated_book.edition)
                self.assertEqual(book_to_update.publication_year, not_updated_book.publication_year)
                self.assertSetEqual(set(book_to_update.authors.all()), set(not_updated_book.authors.all()))

        self.assertEqual(self.books.count(), books_count_before)

    def test_delete(self):
        books_count_before = self.books.count()

        book = self.books.first()

        response = self.delete(book.id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.books.count(), books_count_before - 1)

        retrieve_response = self.retrieve(book.id)

        self.assert404NotFound(retrieve_response)

    def test_delete_invalid(self):
        books_count_before = self.books.count()

        response = self.delete(uuid.uuid4())

        self.assert404NotFound(response)
        self.assertEqual(self.books.count(), books_count_before)
