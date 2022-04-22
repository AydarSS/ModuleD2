from django.forms import ModelForm
from django.template.loader import render_to_string

from .models import Post, User, Category
from django.core.mail import send_mail, EmailMultiAlternatives


# Создаём модельную форму
class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['type', 'title', 'text', 'author','category']

class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['username', 'is_superuser', 'email']

class CategorySubscribeForm (ModelForm):

    class Meta:
        fields = ['category_name']
        model = Category