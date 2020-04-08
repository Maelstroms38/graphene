from graphene_django import DjangoObjectType
from catalog.models import Book, Author

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
		use_connection = True

class AuthorType(DjangoObjectType):
	class Meta:
		model = Author
		only_fields = (
			'first_name',
			'last_name',
			'date_of_birth',
			'date_of_death'
		)
		use_connection = True