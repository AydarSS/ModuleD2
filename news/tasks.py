from datetime import date, timedelta

from celery import shared_task

from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string

from news.models import Post, Category




@shared_task
def send_mail_after_post_add(id):
    post = Post.objects.get(pk=id)
    print(post.id)
    html_content = render_to_string('post_created.html', {'post': post, })
    for category in post.category.all():
        print(category)
        for subscriber in category.subscriber.all():
            print(subscriber)
            msg = EmailMultiAlternatives(
                subject=f'Здравствуй, {subscriber.username}. Новая статья в твоём любимом разделе! {post.title}',
                from_email='xxx@yandex.ru',
                to=[subscriber.email],  # это то же, что и recipients_list
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html
            msg.send()
            print('end')

@shared_task
def send_mail_every_week():
    last_week_date = date.today() - timedelta(days=7)
    dict_sample = {}
    for category in Category.objects.all():
        print(category)
        for subscriber in category.subscriber.all():
            print(subscriber)
            posts = Post.objects.filter(time_in__gt=last_week_date, category=category)
            for post in posts:
                dict_sample[f'http://127.0.0.1:8000/news/{post.id}'] = post.title
            if dict_sample:
                send_mail(
                    subject=f'Привет {subscriber.username} , интересные статьи за неделю',
                    message='; '.join([f'{key}: {value}' for key, value in dict_sample.items()]),
                    from_email='xxx@yandex.ru',
                    recipient_list=[subscriber.email]
                )
            dict_sample.clear()