from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('books/', views.BookListView.as_view(), name='books'),
	path('book/<slug>', views.book_detail, name='book-detail'),
	path('authors/', views.AuthorListView.as_view(), name='authors'),
	path('authors/<slug>', views.AuthorDetailView.as_view(), name='author-detail'),
	path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
	path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
	path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<slug>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<slug>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
	path('book/create/', views.BookCreate.as_view(), name='book_create'),
    path('book/<slug>/update/', views.BookUpdate.as_view(), name='book_update'),
    path('book/<slug>/delete/', views.BookDelete.as_view(), name='book_delete'),
    path('search/', views.search_screen_view, name='search'),
    path('borrowed/', views.BooksBorrowed.as_view(), name='borrowed'),
]
