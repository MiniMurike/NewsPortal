from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from AllNews.models import PostCategory
from main.tasks import send_emails
from .models import Subscription


@receiver(m2m_changed, sender=PostCategory)
def post_created(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        post_categories_qs = instance.post_category.all()

        categories = ''
        subscribers = []
        _request = {}

        for category in post_categories_qs:
            subscribers += (list(
                Subscription.objects.filter(
                    category=category
                ).values_list('user__email', flat=True)))

            categories = f'{category} {categories}'

        _request['categories'] = categories

        # Чистка повторений пользователей, если те указали несколько категорий для рассылки
        subscribers = list(set(subscribers))
        _request['subscribers'] = subscribers

        _request['post_title'] = instance.title
        _request['post_text'] = instance.text
        _request['post_url'] = instance.get_absolute_url()

        send_emails.delay(
            categories=categories,
            subscribers=subscribers,
            post_title=instance.title,
            post_text=instance.text,
            post_url=instance.get_absolute_url(),
        )
