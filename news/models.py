from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.core.cache import cache


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)

    def update_rating(self):
        postRat = self.post_set.all().aggregate(post_rating=Sum('post_rating'))
        pRat = 0
        pRat += postRat.get('post_rating')
        pRat *= 3

        commentRat = self.user.comment_set.all().aggregate(comment_rating=Sum('comment_rating'))
        cRat = 0
        cRat += commentRat.get('comment_rating')

        post_all = self.post_set.all()
        cmRat = 0
        for post in post_all:
            comRat = post.comment_set.all().aggregate(comm_rating=Sum('comment_rating'))
            if comRat.get('comm_rating') is not None:
                cmRat += comRat.get('comm_rating')
        self.rating = pRat+cRat+cmRat
        self.save()

    def __str__(self):
        return f'{self.user.username}'



sport = 'SP'
politic = 'PO'
education = 'ED'
science = 'SC'
CATEGORIES = [
    (sport, 'Спорт'),
    (politic, 'Политика'),
    (education, 'Образование'),
    (science, 'Наука')
]

class Category(models.Model):
    category_name = models.CharField(max_length=2, choices=CATEGORIES, unique=True)
    subscriber = models.ManyToManyField(User, related_name= 'user_subscribers')

    def addsubscriber(self, user):
        self.subscriber.add(user)

    def __str__(self):
        return self.category_name



news = 'NWS'
article = 'ARL'

TYPE = [
    (news, 'новость'),
    (article, 'статья')
]



class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=3, choices=TYPE)
    time_in = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=10000)
    post_rating = models.FloatField(default=0.0)

    category = models.ManyToManyField(Category, through='PostCategory')

    def __str__(self):
        return f'{self.title}'

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return self.text[:123] + '...'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=500, blank=False)
    create_datetime = models.DateTimeField(auto_now_add=True)
    comment_rating = models.FloatField(default=0.0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()




