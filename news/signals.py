from django.core.signals import request_finished
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, PostCategory


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
from .tasks import send_mail_after_post_add


@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == "post_add":
       send_mail_after_post_add.delay(instance.id)
