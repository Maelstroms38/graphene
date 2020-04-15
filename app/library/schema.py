from graphene import Schema, ObjectType
import catalog.gql.schema
import reviews.gql.schema
import users.gql.schema

class Query(catalog.gql.schema.Query, users.gql.schema.Query, ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

class Mutation(catalog.gql.schema.Mutation, reviews.gql.schema.Mutation, users.gql.schema.Mutation, ObjectType):
    # This class will inherit from multiple Mutations
    # as we begin to add more apps to our project
    pass

schema = Schema(query=Query, mutation=Mutation)