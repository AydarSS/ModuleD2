from django.forms import ModelForm
from .models import Post, User


# Создаём модельную форму
class PostForm(ModelForm):


    class Meta:
        model = Post
        fields = ['type', 'title', 'text', 'author']


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['username', 'is_superuser', 'email']