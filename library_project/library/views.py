from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from .filters import AuthorFilter
from .models import Author
from .serializers import AuthorSerializer


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = AuthorFilter
    ordering_fields = ['name']
    ordering = 'name'
