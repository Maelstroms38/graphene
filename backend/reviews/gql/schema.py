from graphene import ObjectType, Schema
from .mutations import ReviewCreate, ReviewDelete

class Mutation(ObjectType):
    create_review = ReviewCreate.Field()
    delete_review = ReviewDelete.Field()

schema = Schema(mutation=Mutation)