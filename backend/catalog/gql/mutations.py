from graphene import Boolean, Field, ID, Mutation
from catalog.models import Book
from .serializers import BookSerializer
from .types import BookType, BookInputType

class BookCreate(Mutation):
    class Arguments:
        input = BookInputType(required=True)
    book = Field(BookType)

    @classmethod
    def mutate(cls, root, info, **data):
        serializer = BookSerializer(data=data.get('input'))
        serializer.is_valid(raise_exception=True)
        return BookCreate(book=serializer.save())

class BookDelete(Mutation):
    class Arguments:
        id = ID(required=True)
    ok = Boolean()

    @classmethod
    def mutate(cls, root, info, **data):
        book = Book.objects.get(id=data.get('id'))
        book.delete()
        return BookDelete(ok=True)