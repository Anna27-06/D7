import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import Post
from datetime import timedelta
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from news.models import Subscription

logger = logging.getLogger(__name__)


# def my_job():
#     today = timezone.now()
#     last_week = today - timedelta(days=7)
#     posts = Post.objects.filter(post_time__gte=last_week).order_by('-post_time')
#     category = set(posts.values_list('category__id', flat=True))
#     subscribers_emails = set(
#         Subscription.objects.filter(category__id__in=category).values_list('user__email', flat=True)
#     )
#
#     for subscriber_email in subscribers_emails:
#         subscriptions_to_category = Subscription.objects.filter(user__email=subscriber_email)
#         list_subscriptions_to_category = set(subscriptions_to_category.values_list('category', flat=True))
#         subscribed_posts = posts.filter(postcategory__category__in=list_subscriptions_to_category).distinct()
#
#         subject = 'Новости и статьи за прошедшую неделю по вашим подпискам'
#         from_email = None
#         to_email = subscriber_email
#
#         text_content = render_to_string(
#             'news_posts_email.txt',
#             {'subscribed_posts': subscribed_posts, 'link': settings.SITE_URL}
#         )
#         html_content = render_to_string(
#             'news_posts_email.html',
#             {'subscribed_posts': subscribed_posts, 'link': settings.SITE_URL}
#         )
#
#         msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
#         msg.attach_alternative(html_content, 'text/html')
#         msg.send()



@util.close_old_connections
def delete_old_job_executions(max_age=604_800):

    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(minute="*/1"),  # Every 10 seconds
            # trigger=CronTrigger(day_of_week="fri", minute="00", hour="18"),  # Every 10 seconds
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")