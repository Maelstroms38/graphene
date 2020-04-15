from graphene import Argument, Field, List, ID, String, Int, ObjectType, Schema
from catalog.models import Author, Book, BookInstance
from .types import BookType, AuthorType, BookInstanceType
from .mutations import BookCreate, BookUpdate, BookDelete, BookInstanceCreate, BookInstanceUpdate, BookInstanceDelete
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class Query(ObjectType):
    books = List(BookType, search=String(), limit=Int(), offset=Int())
    book = Field(BookType, id=Argument(ID, required=True))
    authors = List(AuthorType)
    author = Field(AuthorType, id=Argument(ID, required=True))

    def resolve_books(root, info, search=None, limit=10, offset=0, **kwargs):
        qs = Book.objects.all()
        if search:
            filter = (
                Q(title__icontains=search) |
                Q(isbn__icontains=search)
            )
            return Book.objects.filter(filter)

        return qs[offset:limit+offset]
    
    def resolve_book(root, info, **kwargs):
        return Book.objects.get(id=kwargs.get('id'))

    def resolve_authors(root, info, **kwargs):
        return Author.objects.all()
    
    def resolve_author(root, info, **kwargs):
        return Author.objects.get(id=kwargs.get('id'))

class Mutation(ObjectType):
    create_book = BookCreate.Field()
    update_book = BookUpdate.Field()
    delete_book = BookDelete.Field()
    create_book_instance = BookInstanceCreate.Field()
    update_book_instance = BookInstanceUpdate.Field()
    delete_book_instance = BookInstanceDelete.Field()

schema = Schema(query=Query, mutation=Mutation)