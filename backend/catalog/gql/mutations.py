from graphene import Boolean, Field, ID, Mutation
from catalog.models import Book, Author, Language, Genre
from .serializers import BookSerializer
from .types import BookType, BookInputType
from django.utils.text import slugify

class BookCreate(Mutation):
    class Arguments:
        input = BookInputType(required=True)
    book = Field(BookType)

    @classmethod
    def mutate(cls, root, info, **data):
        data = data.get('input')

        # Initial check for existing book by isbn.
        try:
            book_exists = Book.objects.get(isbn=data.get('isbn'))
            return BookCreate(book=book_exists)
        except:
            pass

        # Author name passed in as string. 
        # Split into first name/last name   
        author_name = data.get('author')
        author_slug = slugify(author_name)
        author_name_split = author_name.split(" ", 1)
        author, created = Author.objects.get_or_create(
            first_name=author_name_split[0], 
            last_name=author_name_split[1], 
            slug=author_slug
        )

        # Language passed in as code.
        # Allow for multi-lingual library.
        language_code = data.get('language')
        language, created = Language.objects.get_or_create(
            slug=language_code,
        )

        genres_arr = data.get('genres')
        genres = []
        for genre in genres_arr:
            genre_obj, created = Genre.objects.get_or_create(name=genre)
            genres.append(genre_obj)

        obj = Book.objects.create(
            title=data.get('title'),
            summary=data.get('summary'),
            isbn=data.get('isbn'),
            image=data.get('image'),
            language=language,
            author=author,
        )
        obj.genre.set(genres)
        
        return BookCreate(book=obj)

class BookDelete(Mutation):
    class Arguments:
        id = ID(required=True)
    ok = Boolean()

    @classmethod
    def mutate(cls, root, info, **data):
        book = Book.objects.get(id=data.get('id'))
        book.delete()
        return BookDelete(ok=True)