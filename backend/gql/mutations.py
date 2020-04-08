from graphene import Boolean, Field, ID, InputObjectType, Mutation, String
from django.contrib.auth import get_user_model
from rest_framework import serializers
from catalog.models import Book
from .types import BookType, UserType

User = get_user_model()

class UserCreate(Mutation):
    user = Field(UserType)

    class Arguments:
        username = String(required=True)
        password = String(required=True)
        email = String(required=True)

    def mutate(self, info, username, password, email):
        user = User(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return UserCreate(user=user)

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            'id',
            'title',
            'summary',
            'isbn',
            'language',
            'author'
        )

class BookInputType(InputObjectType):
    title       = String()
    summary     = String()
    isbn        = String()
    language    = String()
    author      = ID() 

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