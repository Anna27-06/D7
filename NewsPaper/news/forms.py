from django import forms
from .models import Post


class PostFormNews(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'rating', 'author', 'category']


class PostFormArticle(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'rating', 'author', 'category']

