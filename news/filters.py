from django_filters import FilterSet, CharFilter, ModelChoiceFilter, DateFilter
from .models import Post, Author


class PostFilter(FilterSet):
    date = DateFilter(field_name='time_in', lookup_expr='gt')
    title = CharFilter(field_name='title', lookup_expr='icontains')
    author = ModelChoiceFilter(queryset=Author.objects.all())

    class Meta:
        model = Post
        fields = ['date', 'title', 'author']