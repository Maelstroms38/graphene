from graphene_django import DjangoObjectType
from places.models import Place

class PlaceType(DjangoObjectType):
	class Meta:
		model = Place
		only_fields = (
			'id',
			'title',
			'body',
			'created_at'
		)
		use_connection = True