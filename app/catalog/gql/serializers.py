from rest_framework import serializers
from catalog.models import Book, BookInstance

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            'id',
            'title',
            'summary',
            'isbn',
            'language',
            'author',
            'image'
        )

class BookInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInstance
        fields = (
            'id',
            'book',
            'owner',
            'borrower',
            'imprint',
            'due_back',
            'status'
        )