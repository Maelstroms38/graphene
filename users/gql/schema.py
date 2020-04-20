from graphene import Argument, Field, List, ID, String, Int, ObjectType, Schema
from catalog.models import Author, Book, BookInstance
from .types import UserType
from .mutations import UserCreate
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import login_required
import graphql_jwt

User = get_user_model()

class Query(ObjectType):
    current_user = Field(UserType)

    def resolve_users(root, info):
        return User.objects.all()

    @login_required
    def resolve_current_user(root, info):
        user = info.context.user
        return user

class Mutation(ObjectType):
    user_create = UserCreate.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = Schema(query=Query, mutation=Mutation)