from graphene_django import DjangoObjectType
from graphene import InputObjectType, String, Int, ID 
from reviews.models import Review

class ReviewType(DjangoObjectType):
	class Meta:
		model = Review

class ReviewInputType(InputObjectType):
    user        = ID()
    comment     = String()
    value       = Int()
    book        = ID()