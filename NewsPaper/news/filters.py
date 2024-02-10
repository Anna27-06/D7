from django_filters import FilterSet, ModelChoiceFilter, CharFilter, DateFilter
from .models import Post, Category
from django.forms import DateTimeInput


class PostFilter(FilterSet):
    title = CharFilter(
        lookup_expr='iexact',
        label='Заголовок'
    )
    category = ModelChoiceFilter(
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Выберите категорию'
    )
    post_time = DateFilter(
        lookup_expr='gt',
        widget=DateTimeInput({'type': 'date'}),
        label='Позже указываемой даты'
    )

    # class Meta:
    #     model = Post
    #     fields = ['title', 'category', 'post_time']
