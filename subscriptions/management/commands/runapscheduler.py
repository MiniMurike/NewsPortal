import datetime
import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from subscriptions.models import Subscription
from AllNews.models import Post


logger = logging.getLogger(__name__)


def send_last_posts():
    today = datetime.datetime.utcnow()
    last_week = today - datetime.timedelta(days=7)

    posts = Post.objects.filter(
        date__gte=last_week
    ).exclude(
        post_category__isnull=True
    )

    categories = set(posts.values_list('postcategory__category__category', flat=True))
    subscribers_email = set(Subscription.objects.filter(
        category__category__in=categories
    ).values_list('user__email', flat=True))

    html_content = render_to_string(
        'weekly_posts.html',
        {
            'link': 'http://localhost:8000',
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=None,
        to=subscribers_email
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_last_posts,
            trigger=CronTrigger(
                day_of_week='fri', hour='18', minute='00'
            ),
            # trigger=CronTrigger(
            #     second='00'
            # ),
            id="send_last_posts",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'send_last_posts'.")

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