from graphene import ObjectType, Schema
from .mutations import ReviewCreate, ReviewUpdate, ReviewDelete

class Mutation(ObjectType):
    create_review = ReviewCreate.Field()
    update_review = ReviewUpdate.Field()
    delete_review = ReviewDelete.Field()

schema = Schema(mutation=Mutation)