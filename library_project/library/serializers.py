from rest_framework import serializers

from library.models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'edition', 'publication_year', 'authors']

    def to_representation(self, book: Book):
        book_representation = super().to_representation(book)

        book_representation['authors'] = self.serialize_authors(book)

        return book_representation

    def serialize_authors(self, book: Book):
        serializer = AuthorSerializer(book.authors, many=True)
        return serializer.data
