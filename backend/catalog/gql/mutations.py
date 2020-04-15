from graphene import Boolean, Field, ID, Mutation
from catalog.models import Book, Author, Language, Genre, BookInstance
from .serializers import BookSerializer, BookInstanceSerializer
from .types import BookType, BookInputType, BookInstanceType, BookInstanceInputType
from django.utils.text import slugify
from graphql_jwt.decorators import login_required, permission_required

class BookCreate(Mutation):
    book = Field(BookType)
    class Arguments:
        input = BookInputType(required=True)

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

class BookUpdate(Mutation):
    book = Field(BookType)
    class Arguments:
        input = BookInputType(required=True)

    @classmethod
    @permission_required('catalog.can_mark_returned')
    def mutate(cls, root, info, **data):
        input_data = data.get('input')
        book = Book.objects.get(id=input_data.get('id'))
        serializer = BookSerializer(book, data=input_data)
        serializer.is_valid(raise_exception=True)
        return BookUpdate(book=serializer.save())

class BookDelete(Mutation):
    ok = Boolean()
    class Arguments:
        id = ID(required=True)

    @classmethod
    @permission_required('catalog.can_mark_returned')
    def mutate(cls, root, info, **data):
        book = Book.objects.get(id=data.get('id'))
        book.delete()
        return BookDelete(ok=True)

class BookInstanceCreate(Mutation):
    instance = Field(BookInstanceType)
    class Arguments:
        input = BookInstanceInputType(required=True)

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        book_data = data.get('input')
        book_data['owner'] = user.id 

        serializer = BookInstanceSerializer(data=book_data)
        serializer.is_valid(raise_exception=True)
        return BookInstanceCreate(instance=serializer.save())

class BookInstanceUpdate(Mutation):
    instance = Field(BookInstanceType)
    class Arguments:
        input = BookInstanceInputType(required=True)

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        input_data = data.get('input')
        book = BookInstance.objects.get(id=input_data.get('id'), owner=user)
        serializer = BookInstanceSerializer(book, data=input_data)
        serializer.is_valid(raise_exception=True)
        return BookInstanceUpdate(instance=serializer.save())

class BookInstanceDelete(Mutation):
    ok = Boolean()
    class Arguments:
        id = ID(required=True)

    @classmethod
    @login_required
    def mutate(cls, root, info, **data):
        user = info.context.user
        book = BookInstance.objects.get(id=data.get('id'), owner=user)
        book.delete()
        return BookInstanceDelete(ok=True)