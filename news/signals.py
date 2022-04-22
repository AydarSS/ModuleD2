from django.core.signals import request_finished
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, PostCategory


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == "post_add":
        html_content = render_to_string('post_created.html',{'post': instance,} )
        for category in instance.category.all():
            print(category)
            for subscriber in category.subscriber.all():
                print(subscriber)
                msg = EmailMultiAlternatives(
                    subject=f'Здравствуй, {subscriber.username}. Новая статья в твоём любимом разделе! {instance.title}',
                    from_email='xxx@yandex.ru',
                    to=[subscriber.email],  # это то же, что и recipients_list
                )
                msg.attach_alternative(html_content, "text/html")  # добавляем html
                msg.send()
                print('end')