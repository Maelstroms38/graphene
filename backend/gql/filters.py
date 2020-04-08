from django.db.models import Q
import django_filters
from catalog.models import Book

class BookFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    class Meta:
        model = Book
        fields = ()

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | Q(isbn__icontains=value)
        )