import datetime
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from AllNews.models import Post
from main.celery import app
from subscriptions.models import Subscription


@app.task()
def send_emails(**args):
    subject = f'Новая запись в категории {args["categories"]}'

    text_content = '\n'.join([
        f'Заголовок: {args["post_title"]}',
        f'Содержание: {args["post_text"][:15]}...\n',
        f'Подробнее...->: http://localhost:8000{args["post_url"]}',
    ])

    html_content = '<br>'.join([
        f'Заголовок: {args["post_title"]}',
        f'Содержание: {args["post_text"][:15]}...<br>',
        f'<a href="http://localhost:8000{args["post_url"]}">Подробнее...-></a>'
    ])

    for email in args['subscribers']:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=None,
            to=[email]
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@shared_task
def send_weekly_newsletter():
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

    for user in subscribers_email:
        msg = EmailMultiAlternatives(
            subject='Статьи за неделю',
            body='',
            from_email=None,
            to=[user]
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
