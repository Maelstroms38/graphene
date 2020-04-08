from graphene import Argument, Field, List, ID, ObjectType, Schema
from graphene_django.filter import DjangoFilterConnectionField
from catalog.models import Author, Book, BookInstance
from .types import BookType, AuthorType
from .filters import BookFilter
from .mutations import BookCreate, BookDelete

class Query(ObjectType):
    books = DjangoFilterConnectionField(BookType, filterset_class=BookFilter)
    book = Field(BookType, id=Argument(ID, required=True))
    authors = List(AuthorType)
    author = Field(AuthorType, id=Argument(ID, required=True))
    
    def resolve_books(root, info, **kwargs):
        return Book.objects.all()
    
    def resolve_book(root, info, **kwargs):
        return Book.objects.get(id=kwargs.get('id'))

    def resolve_authors(root, info, **kwargs):
        return Author.objects.all()
    
    def resolve_author(root, info, **kwargs):
        return Author.objects.get(id=kwargs.get('id'))

class Mutation(ObjectType):
	create_book = BookCreate.Field()
	delete_book = BookDelete.Field()

schema = Schema(query=Query, mutation=Mutation)