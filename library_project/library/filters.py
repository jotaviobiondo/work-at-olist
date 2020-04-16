from django_filters import rest_framework as filters

from library.models import Author, Book


class AuthorFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Author
        fields = ['name']


class BookFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    author = filters.CharFilter(field_name='authors__name', lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['edition', 'publication_year']
