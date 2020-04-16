from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from .filters import AuthorFilter, BookFilter
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = AuthorFilter
    ordering_fields = ['name']
    ordering = 'name'


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = BookFilter
    ordering_fields = ['name', 'edition', 'publication_year', 'authors__name']
    ordering = 'name'
