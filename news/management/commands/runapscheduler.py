import logging
from datetime import timedelta, date

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from news.models import Post, Category


logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    last_week_date = date.today()-timedelta(days=7)
    dict_sample = {}
    for category in  Category.objects.all():
        print(category)
        for subscriber in category.subscriber.all():
            print(subscriber)
            posts = Post.objects.filter(time_in__gt=last_week_date, category = category)
            for post in posts:

                dict_sample[f'http://127.0.0.1:8000/news/{post.id}'] = post.title
            if dict_sample:
                send_mail(
                  subject=f'Привет {subscriber.username} , интересные статьи за неделю',
                  message= '; '.join([f'{key}: {value}' for key, value in dict_sample.items()]),
                  from_email='xxx@yandex.ru',
                  recipient_list=[subscriber.email]
                  )
            dict_sample.clear()



# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")