import datetime
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from AllNews.models import Post
from subscriptions.models import Subscription


@shared_task
def send_emails(instance):
    post_categories_qs = instance.post_category.all()

    categories = ''
    subscribers = []

    for category in post_categories_qs:
        subscribers += (list(
            Subscription.objects.filter(
                category=category
            ).values_list('user__email', flat=True)))

        categories = f'{category} {categories}'

    # Чистка повторений пользователей, если те указали несколько категорий для рассылки
    subscribers = list(set(subscribers))

    subject = f'Новая запись в категории {categories}'

    text_content = '\n'.join([
        f'Заголовок: {instance.title}',
        f'Содержание: {instance.text[:15]}...\n',
        f'Подробнее...->: http://localhost:8000{instance.get_absolute_url()}',
    ])

    html_content = '<br>'.join([
        f'Заголовок: {instance.title}',
        f'Содержание: {instance.text[:15]}...<br>',
        f'<a href="http://localhost:8000{instance.get_absolute_url()}">Подробнее...-></a>'
    ])

    for email in subscribers:
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

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=None,
        to=subscribers_email
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
