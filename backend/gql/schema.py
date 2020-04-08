from graphene import Argument, Field, List, ID, String, Int, ObjectType, Schema
from catalog.models import Author, Book, BookInstance
from .types import BookType, AuthorType, UserType
from .mutations import BookCreate, BookDelete, UserCreate
from django.contrib.auth import get_user_model
from django.db.models import Q
import graphql_jwt

User = get_user_model()

class Query(ObjectType):
    books = List(BookType, search=String(), limit=Int(), offset=Int())
    book = Field(BookType, id=Argument(ID, required=True))
    authors = List(AuthorType)
    author = Field(AuthorType, id=Argument(ID, required=True))
    current_user = Field(UserType)
    
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

    def resolve_users(root, info):
        return User.objects.all()

    def resolve_current_user(root, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        return user


class Mutation(ObjectType):
    create_book = BookCreate.Field()
    delete_book = BookDelete.Field()
    create_user = UserCreate.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = Schema(query=Query, mutation=Mutation)