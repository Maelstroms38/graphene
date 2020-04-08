from django.contrib import admin

# Register your models here.
from .models import Author, Book, BookInstance, Genre, Language

classes = [Author, Book, BookInstance, Genre, Language]

for c in classes:
	admin.site.register(c)