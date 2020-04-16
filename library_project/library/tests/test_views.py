import uuid

from rest_framework import status
from rest_framework.test import APITestCase

from library.models import Author


class BaseRestApiTest(APITestCase):
    base_url = None

    def list(self, query=None):
        if query is None:
            query = {}

        return self.client.get(self.base_url, query, format='json')

    def retrieve(self, resource_id):
        return self.client.get(self.base_url + f'{resource_id}/', format='json')

    def create(self, payload=None):
        if payload is None:
            payload = {}

        return self.client.post(self.base_url, payload, format='json')

    def update(self, resource_id, payload=None):
        if payload is None:
            payload = {}

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


class AuthorsApiTest(BaseRestApiTest):
    author_names = [
        'Luciano Ramalho',
        'Osvaldo Santana Neto',
        'David Beazley',
        'Chetan Giridhar',
        'Brian K. Jones',
        'J.K Rowling'
    ]

    base_url = '/api/authors/'

    @classmethod
    def setUpTestData(cls):
        for name in cls.author_names:
            Author.objects.create(name=name)

        cls.authors = Author.objects.all()

    def test_list(self):
        response = self.list()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], self.authors.count())

    def test_list_page_query_params(self):
        self.assertPaginatedListQueryParams('page', 'page_size')

    def test_retrieve(self):
        author = self.authors.first()

        response = self.retrieve(author.id)

        serializable_fields = ['id', 'name']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual(response.data.keys(), serializable_fields)
        self.assertEqual(response.data['id'], str(author.id))
        self.assertEqual(response.data['name'], author.name)

    def test_retrieve_nonexistent(self):
        random_uuid = uuid.uuid4()
        response = self.retrieve(random_uuid)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_search_name(self):
        author = self.authors.first()

        partial_name = author.name[:5]

        query = {'name': partial_name}
        response = self.list(query)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data['results']
        matched_result = next((result for result in results if result['id'] == str(author.id)), None)

        self.assertIsNotNone(matched_result)
        self.assertEqual(matched_result['name'], author.name)

    def test_search_name_nonexistent(self):
        query = {'name': 'Nonexistent Author'}
        response = self.list(query)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertListEqual(response.data['results'], [])
