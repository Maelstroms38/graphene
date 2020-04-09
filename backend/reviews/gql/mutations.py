from graphene import Boolean, Field, ID, Mutation
from django.contrib.auth import get_user_model

from .types import ReviewType, ReviewInputType
from .serializers import ReviewSerializer

User = get_user_model()

class ReviewCreate(Mutation):
    review = Field(ReviewType)
    class Arguments:
        input = ReviewInputType(required=True)

    @classmethod
    def mutate(cls, root, info, **data):
        serializer = ReviewSerializer(data=data.get('input'))
        serializer.is_valid(raise_exception=True)
        return ReviewCreate(review=serializer.save())

class ReviewDelete(Mutation):
    class Arguments:
        id = ID(required=True)
    ok = Boolean()

    @classmethod
    def mutate(cls, root, info, **data):
        review = Review.objects.get(id=data.get('id'))
        review.delete()
        return ReviewDelete(ok=True)