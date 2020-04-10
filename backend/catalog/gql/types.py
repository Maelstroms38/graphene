from graphene import InputObjectType, String, ID, List
from graphene_django import DjangoObjectType
from catalog.models import Book, Author, Genre, Language

class BookInputType(InputObjectType):
    title       = String()
    summary     = String()
    isbn        = String()
    image       = String()
    language    = String()
    author      = String() 
    genres      = List(String)

class GenreType(DjangoObjectType):
    class Meta:
        model = Genre

class LanguageType(DjangoObjectType):
    class Meta:
        model = Language

class BookType(DjangoObjectType):
	class Meta:
		model = Book

class AuthorType(DjangoObjectType):
	class Meta:
		model = Author