from graphene import InputObjectType, String, ID, List
from graphene_django import DjangoObjectType
from catalog.models import Book, BookInstance, Author, Genre, Language

class BookInputType(InputObjectType):
    id          = ID()
    title       = String()
    summary     = String()
    isbn        = String()
    image       = String()
    language    = String()
    author      = String() 
    genres      = List(String)

class BookInstanceInputType(InputObjectType):
    id       = ID()
    book     = ID()
    borrower = ID()
    imprint  = String()
    due_back = String()
    status   = String()

class GenreType(DjangoObjectType):
    class Meta:
        model = Genre

class LanguageType(DjangoObjectType):
    class Meta:
        model = Language

class BookType(DjangoObjectType):
	class Meta:
		model = Book

class BookInstanceType(DjangoObjectType):
    class Meta:
        model = BookInstance

class AuthorType(DjangoObjectType):
	class Meta:
		model = Author