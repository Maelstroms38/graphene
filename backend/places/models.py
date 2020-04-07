from django.db import models

# Create your models here.

class Place(models.Model):
	title 				= models.CharField(max_length=255)
	body 				= models.TextField()
	created_at  		= models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-created_at', )

	def __str__(self):
		return '{} (#{})'.format(self.title, self.pk) 
