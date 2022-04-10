from django.contrib import admin
from django.urls import path
# Импортируем созданное нами представление
from .views import PostsList, PostsListSearch, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, ProfileUpdateView

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.

   path('', PostsList.as_view()),
   path('search', PostsListSearch.as_view()),
   path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),  # Ссылка на детали товара
   path('create/', PostCreateView.as_view(), name='post_create'),  # Ссылка на создание товара
   path('create/<int:pk>', PostUpdateView.as_view(), name='post_update'),
   path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
   path('user_update/', ProfileUpdateView.as_view(), name='profile_update'),


]