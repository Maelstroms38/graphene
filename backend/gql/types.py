from graphene_django import DjangoObjectType
from catalog.models import Book, Author
from django.contrib.auth import get_user_model

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class BookType(DjangoObjectType):
	class Meta:
		model = Book
		only_fields = (
			'id',
			'isbn',
			'title',
			'author',
			'summary',
		)

class AuthorType(DjangoObjectType):
	class Meta:
		model = Author
		only_fields = (
			'first_name',
			'last_name',
			'date_of_birth',
			'date_of_death'
		)