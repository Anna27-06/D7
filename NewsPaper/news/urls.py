from django.urls import path
# Импортируем созданное нами представление
from .views import PostsList, PostDetail, PostSearch, PostCreateNews, PostCreateArticle, PostsUpdateNews, PostsUpdateArticles, PostsDeleteNews, PostsDeleteArticles, subscriptions

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('posts/', PostsList.as_view(), name='posts_list'),
   path('posts/<int:pk>/', PostDetail.as_view(), name='posts_detail'),
   path('posts/search/', PostSearch.as_view(), name='post_search'),
   path('posts/create/', PostCreateNews.as_view(), name='post_create'),
   path('posts/<int:pk>/edit/', PostsUpdateNews.as_view(), name='post_update'),
   path('posts/<int:pk>/delete/', PostsDeleteNews.as_view(), name='post_delete'),

   path('articles/create/', PostCreateArticle.as_view(), name='articles_create'),
   path('articles/<int:pk>/', PostDetail.as_view(), name='articles_detail'),
   path('articles/<int:pk>/edit/', PostsUpdateArticles.as_view(), name='articles_update'),
   path('articles/<int:pk>/delete/', PostsDeleteArticles.as_view(), name='articles_delete'),
   path('subscriptions/', subscriptions, name='subscriptions'),
]